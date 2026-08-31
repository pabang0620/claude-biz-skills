#!/usr/bin/env python3
"""
sales-data-analyzer 보조 스크립트

주문 CSV를 읽어 KPI, 기간 비교, RFM 세그먼트, 상품별 특이사항을 계산해
JSON으로 표준출력한다. 외부 패키지(pandas 등) 없이 표준 라이브러리만 사용한다.

사용법:
    python3 analyze.py <csv경로> [--split-date YYYY-MM-DD] [--encoding utf-8]

옵션:
    --split-date  "이번 기간"과 "직전 기간"을 나누는 기준일(이 날짜 포함 이후=이번 기간).
                  생략하면 데이터의 최소~최대 날짜 구간을 절반으로 나눈다.
    --encoding    CSV 인코딩. 기본 utf-8-sig. cp949(EUC-KR)로 저장된 국내 쇼핑몰
                  다운로드 파일이면 --encoding cp949 로 재시도한다.

출력(JSON)은 Claude가 그대로 읽어 HTML 템플릿의 숫자를 채우는 데 쓴다.
컬럼을 못 찾은 항목은 값 대신 null이 들어가므로, 리포트에는 "산출 불가"로
표기하고 절대 임의 수치로 채우지 않는다.
"""
import sys
import csv
import json
import argparse
from datetime import datetime

# ---------------------------------------------------------------------------
# 1. 컬럼 매핑 - 플랫폼마다 헤더명이 다르므로 유사어 사전으로 탐색한다.
# ---------------------------------------------------------------------------
COLUMN_ALIASES = {
    "date": [
        "주문일자", "주문일시", "결제일", "결제일시", "발주일", "order_date",
        "date", "purchase_date", "일자", "orderdate",
    ],
    "product": [
        "상품명", "상품", "품목명", "품목", "product_name", "product", "item_name",
        "옵션상품명",
    ],
    "amount": [
        "금액", "결제금액", "총금액", "주문금액", "판매금액", "합계금액", "결제액",
        "amount", "price", "total", "총 주문금액", "정산금액",
    ],
    "customer": [
        "이메일", "email", "고객id", "고객ID", "구매자", "구매자id", "구매자ID",
        "customer_id", "고객번호", "전화번호", "phone", "user_id", "아이디",
        "회원번호",
    ],
}


def find_column(header, key):
    """header 목록에서 key(date/product/amount/customer)에 해당하는 실제 컬럼명을 찾는다."""
    header_norm = [h.strip().lower() for h in header]
    for alias in COLUMN_ALIASES[key]:
        alias_norm = alias.strip().lower()
        for i, h in enumerate(header_norm):
            if alias_norm == h or alias_norm in h:
                return header[i]
    return None


def parse_amount(raw):
    if raw is None:
        return None
    s = str(raw).replace(",", "").replace("원", "").replace("₩", "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_date(raw):
    s = str(raw).strip()
    if not s:
        return None
    fmts = [
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S", "%Y/%m/%d",
        "%Y.%m.%d", "%Y%m%d",
    ]
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# 2. 로드
# ---------------------------------------------------------------------------
def load_rows(path, encoding):
    with open(path, newline="", encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader)
        col_date = find_column(header, "date")
        col_product = find_column(header, "product")
        col_amount = find_column(header, "amount")
        col_customer = find_column(header, "customer")

        idx = {name: header.index(name) for name in
               [c for c in [col_date, col_product, col_amount, col_customer] if c]}

        rows = []
        skipped = 0
        for r in reader:
            if not r or len(r) < len(header):
                skipped += 1
                continue
            d = parse_date(r[idx[col_date]]) if col_date else None
            amt = parse_amount(r[idx[col_amount]]) if col_amount else None
            prod = r[idx[col_product]].strip() if col_product else None
            cust = r[idx[col_customer]].strip() if col_customer else None
            if d is None or amt is None:
                skipped += 1
                continue
            rows.append({"date": d, "product": prod, "amount": amt, "customer": cust})

        mapping = {
            "date": col_date, "product": col_product,
            "amount": col_amount, "customer": col_customer,
        }
        return rows, mapping, skipped


# ---------------------------------------------------------------------------
# 3. KPI
# ---------------------------------------------------------------------------
def compute_kpi(rows):
    if not rows:
        return None
    total_revenue = sum(r["amount"] for r in rows)
    total_orders = len(rows)
    aov = total_revenue / total_orders if total_orders else 0

    has_customer = any(r["customer"] for r in rows)
    repeat_rate = None
    new_ratio = None
    repeat_ratio = None
    if has_customer:
        by_cust = {}
        for r in rows:
            if not r["customer"]:
                continue
            by_cust.setdefault(r["customer"], []).append(r)
        n_cust = len(by_cust)
        n_repeat = sum(1 for orders in by_cust.values() if len(orders) >= 2)
        if n_cust:
            repeat_rate = round(n_repeat / n_cust * 100, 1)
            new_ratio = round((n_cust - n_repeat) / n_cust * 100, 1)
            repeat_ratio = round(n_repeat / n_cust * 100, 1)

    return {
        "total_revenue": round(total_revenue),
        "total_orders": total_orders,
        "avg_order_value": round(aov),
        "repeat_rate_pct": repeat_rate,
        "new_customer_pct": new_ratio,
        "repeat_customer_pct": repeat_ratio,
    }


# ---------------------------------------------------------------------------
# 4. 기간 비교
# ---------------------------------------------------------------------------
def split_period(rows, split_date):
    dates = [r["date"] for r in rows]
    min_d, max_d = min(dates), max(dates)
    if split_date is None:
        split_date = min_d + (max_d - min_d) / 2
    current = [r for r in rows if r["date"] >= split_date]
    previous = [r for r in rows if r["date"] < split_date]
    return current, previous, min_d, max_d, split_date


# ---------------------------------------------------------------------------
# 5. RFM - 단순 규칙 기반 (percentile 계산에 외부 라이브러리 불필요하게 직접 구현)
# ---------------------------------------------------------------------------
def percentile(sorted_vals, pct):
    if not sorted_vals:
        return 0
    k = (len(sorted_vals) - 1) * pct
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def compute_rfm(rows, as_of_date):
    if not any(r["customer"] for r in rows):
        return None

    by_cust = {}
    for r in rows:
        if not r["customer"]:
            continue
        by_cust.setdefault(r["customer"], []).append(r)

    monetary_all = sorted(sum(o["amount"] for o in orders) for orders in by_cust.values())
    m33 = percentile(monetary_all, 0.33)
    m66 = percentile(monetary_all, 0.66)

    def r_grade(days):
        if days <= 30:
            return 3
        if days <= 90:
            return 2
        return 1

    def f_grade(cnt):
        if cnt >= 3:
            return 3
        if cnt == 2:
            return 2
        return 1

    def m_grade(amt):
        if amt >= m66:
            return 3
        if amt >= m33:
            return 2
        return 1

    def segment(rg, fg, mg):
        # 우선순위 규칙(위에서부터 먼저 맞는 것을 채택)
        if rg == 1 and fg == 1 and mg == 1:
            return "휴면/이탈"
        if rg == 1 and (fg >= 2 or mg >= 2):
            return "이탈위험"
        if fg == 1 and rg == 3:
            return "신규고객"
        if fg == 1 and mg == 3 and rg >= 2:
            return "잠재우수(첫구매 고액)"
        if rg == 3 and fg == 3 and mg == 3:
            return "최우수고객"
        if rg >= 2 and fg >= 2:
            return "충성고객"
        return "일반고객"

    counts = {}
    for cust, orders in by_cust.items():
        last_purchase = max(o["date"] for o in orders)
        recency_days = (as_of_date - last_purchase).days
        frequency = len(orders)
        monetary = sum(o["amount"] for o in orders)
        seg = segment(r_grade(recency_days), f_grade(frequency), m_grade(monetary))
        counts[seg] = counts.get(seg, 0) + 1

    total = sum(counts.values())
    result = []
    for seg, cnt in sorted(counts.items(), key=lambda kv: -kv[1]):
        result.append({
            "segment": seg,
            "count": cnt,
            "pct": round(cnt / total * 100, 1) if total else 0,
        })
    return result


# ---------------------------------------------------------------------------
# 6. 상품별 특이사항 (이번 기간 vs 직전 기간 매출 증감)
# ---------------------------------------------------------------------------
def compute_anomalies(current, previous, min_share=0.03):
    if not current and not previous:
        return {"up": [], "down": []}

    def by_product(rows):
        d = {}
        for r in rows:
            if not r["product"]:
                continue
            d[r["product"]] = d.get(r["product"], 0) + r["amount"]
        return d

    cur = by_product(current)
    prev = by_product(previous)
    total_cur = sum(cur.values()) or 1

    changes = []
    for prod in set(list(cur.keys()) + list(prev.keys())):
        c = cur.get(prod, 0)
        p = prev.get(prod, 0)
        if c / total_cur < min_share and p / total_cur < min_share:
            continue  # 매출 비중이 너무 작은 상품은 노이즈로 제외
        if p == 0 and c == 0:
            continue
        if p == 0:
            pct_change = None  # 직전 기간 매출 0 -> 신규 등장, 배율 계산 불가
        else:
            pct_change = round((c - p) / p * 100, 1)
        changes.append({
            "product": prod, "current": round(c), "previous": round(p),
            "pct_change": pct_change,
        })

    up = sorted([c for c in changes if c["pct_change"] is not None and c["pct_change"] > 0],
                key=lambda c: -c["pct_change"])[:3]
    down = sorted([c for c in changes if c["pct_change"] is not None and c["pct_change"] < 0],
                  key=lambda c: c["pct_change"])[:3]
    return {"up": up, "down": down}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--split-date", default=None, help="YYYY-MM-DD")
    ap.add_argument("--encoding", default="utf-8-sig")
    args = ap.parse_args()

    split_date = parse_date(args.split_date) if args.split_date else None

    try:
        rows, mapping, skipped = load_rows(args.csv_path, args.encoding)
    except UnicodeDecodeError:
        sys.stderr.write(
            "utf-8 디코딩 실패. --encoding cp949 로 재시도하세요 (국내 쇼핑몰 CSV는 EUC-KR/CP949인 경우가 많음).\n"
        )
        sys.exit(1)

    if not rows:
        print(json.dumps({
            "error": "유효한 행을 찾지 못했습니다. 컬럼 매핑을 확인하세요.",
            "column_mapping": mapping,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    current, previous, min_d, max_d, used_split = split_period(rows, split_date)

    result = {
        "meta": {
            "row_count": len(rows),
            "skipped_rows": skipped,
            "column_mapping": mapping,
            "date_range": [min_d.strftime("%Y-%m-%d"), max_d.strftime("%Y-%m-%d")],
            "split_date": used_split.strftime("%Y-%m-%d"),
        },
        "kpi_total": compute_kpi(rows),
        "period_comparison": {
            "current": compute_kpi(current),
            "previous": compute_kpi(previous),
        },
        "rfm_segments": compute_rfm(rows, max_d),
        "anomalies": compute_anomalies(current, previous),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
