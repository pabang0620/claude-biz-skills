---
name: sales-data-analyzer
description: 스마트스토어·쿠팡·자사몰 등에서 받은 주문/매출 CSV를 KPI·기간 비교·RFM 고객 세그먼트 리포트로 자동 변환하는 스킬. "매출 CSV 분석해줘", "주문 데이터 리포트 만들어줘", "판매 데이터 분석", "재구매율 분석", "RFM 분석", "sales data analysis" 같은 요청 시 활성화한다. 사람이 엑셀로 피벗하지 않아도 총매출·주문건수·객단가·재구매율과 고객 세그먼트(최우수/충성/신규/이탈위험/휴면)까지 인쇄 최적화 HTML 리포트 1장으로 뽑는다.
version: 1.0.0
triggers:
  - /sales-data-analyzer
  - 매출 분석
  - 주문 데이터 분석
---

# sales-data-analyzer 스킬

## 역할

주문 CSV(스마트스토어·쿠팡·자사몰 등, 플랫폼마다 컬럼 구성이 다름) 1개를 입력받아, 사람이 엑셀로 일일이 피벗하지 않아도 되도록 다음을 자동 계산해 **A4 인쇄 최적화 HTML 리포트 1장**으로 만든다.

1. 핵심 KPI(총매출·주문건수·객단가·재구매율·신규 대비 재구매고객 비중)
2. 이번 기간 vs 직전 기간 비교
3. RFM(Recency·Frequency·Monetary) 기준 고객 세그먼트와 세그먼트별 고객 수
4. 데이터에서 자동 발견된 상품별 매출 급증/급감 특이사항

`quote-comparison`과 같은 계열이며 색상 팔레트·인쇄 스타일 컨벤션(`@page A4`, 화면 전용 인쇄 안내바, `@media screen/print` 분기, 네이비+골드)을 그대로 따른다. 차이는 견적 비교표가 아니라 **CSV 원자료를 직접 집계**한다는 점이다.

## 산출물

- `매출분석_<대상>_<작성일>.html` (지정 경로 또는 `docs/매출분석/`)
- 사용자가 크롬에서 `Ctrl+P → PDF로 저장`(배경 그래픽 ON)으로 PDF화

## 입력

- 주문 CSV 1개. 최소한 **주문일자·상품명·금액·고객식별자(이메일 또는 ID)** 정도는 있다고 가정하고, 컬럼명이 플랫폼마다 다르면 유사 컬럼을 찾아 매핑한다(아래 "1단계" 참고).
- 고객식별자 컬럼이 아예 없으면 재구매율·RFM 세그먼트는 산출 불가 - 임의로 추정하지 말고 리포트에 "고객 식별 컬럼 없음 - 산출 불가"로 명시한다.

## 참조 파일

- `assets/analyze.py` - 컬럼 매핑, KPI, 기간 비교, RFM, 상품별 특이사항을 계산해 JSON으로 출력하는 표준 라이브러리 전용 파이썬 스크립트. **직접 산수하지 말고 이 스크립트를 Bash로 실행해서 나온 숫자를 템플릿에 채운다.** (필요할 때만 읽는다 - 커스터마이징이 필요할 때, 예: 컬럼 유사어 사전에 새 표현을 추가할 때)

## 1단계: 컬럼 매핑

CSV 헤더를 읽고 아래 유사어에 해당하는 컬럼을 찾는다(`assets/analyze.py`의 `COLUMN_ALIASES`에 이미 구현되어 있으므로 스크립트를 그대로 실행하면 자동으로 매핑된다. 사전에 없는 낯선 헤더명을 만나면 스크립트의 `COLUMN_ALIASES`에 한 줄 추가하고 다시 실행한다):

| 키 | 유사어 예시 |
|---|---|
| 주문일자 | 주문일자, 주문일시, 결제일, 결제일시, 발주일, order_date, date |
| 상품명 | 상품명, 상품, 품목명, product_name, item_name |
| 금액 | 금액, 결제금액, 총금액, 주문금액, 판매금액, amount, price, total |
| 고객식별자 | 이메일, email, 고객ID, 구매자, customer_id, 전화번호, 회원번호 |

매핑이 애매하거나(예: "금액" 유사 컬럼이 2개 이상 발견) 값 형식이 예상과 다르면(날짜가 아닌 텍스트, 통화기호가 섞인 숫자 등) 임의로 하나를 고르지 말고 사용자에게 어느 컬럼인지 확인한다.

## 2단계: 스크립트 실행

```bash
python3 <스킬경로>/assets/analyze.py <CSV경로>
# 국내 쇼핑몰 다운로드 CSV가 EUC-KR이면:
python3 <스킬경로>/assets/analyze.py <CSV경로> --encoding cp949
# 기간 구분 기준일을 직접 지정하고 싶으면:
python3 <스킬경로>/assets/analyze.py <CSV경로> --split-date 2026-08-16
```

`--split-date`를 생략하면 스크립트가 데이터 전체 기간(최소~최대 날짜)의 정중앙 날짜를 기준으로 "이번 기간"/"직전 기간"을 자동으로 반으로 나눈다. 데이터 기간이 너무 짧아(예: 하루치) 의미 있는 기간 비교가 안 되면, 출력 JSON의 `period_comparison.previous.total_orders`가 0에 가까울 것이므로 그 경우 리포트의 기간 비교 섹션 대신 "데이터 기간이 짧아 기간 비교 생략"으로 표기한다.

출력 JSON에서 그대로 쓸 값:
- `kpi_total` → 상단 KPI 칩 5종
- `period_comparison.current` / `.previous` → 기간 비교 2컬럼
- `rfm_segments` → RFM 세그먼트 표 (세그먼트명·고객수·비중)
- `anomalies.up` / `.down` → 특이사항 콜아웃

## 3단계: RFM 세그먼트 판정 기준 (스크립트에 이미 구현됨 - 참고용)

- **Recency(최근성)**: 분석 기준일(데이터의 최신 주문일) 대비 마지막 구매일 경과일. 30일 이내=고(3), 31~90일=중(2), 91일 초과=저(1).
- **Frequency(구매빈도)**: 전체 기간 구매 횟수. 3회 이상=고(3), 2회=중(2), 1회=저(1).
- **Monetary(구매금액)**: 고객별 총 구매액을 정렬해 상위 33%=고(3), 중간 33%=중(2), 하위 33%=저(1) (데이터셋마다 금액 스케일이 다르므로 절대 기준이 아니라 상대 순위로 계산).
- 세그먼트는 아래 우선순위 규칙을 위에서부터 순서대로 적용해 첫 번째로 맞는 것을 채택한다.

| 순위 | 조건 | 세그먼트 |
|---|---|---|
| 1 | R=1 & F=1 & M=1 | 휴면/이탈 |
| 2 | R=1 & (F≥2 또는 M≥2) | 이탈위험 (과거엔 활발했으나 최근 이탈) |
| 3 | F=1 & R=3 | 신규고객 (최근 첫 구매) |
| 4 | F=1 & M=3 & R≥2 | 잠재우수 (첫 구매인데 고액) |
| 5 | R=3 & F=3 & M=3 | 최우수고객 |
| 6 | R≥2 & F≥2 | 충성고객 |
| 7 | 그 외 | 일반고객 |

이 표는 발주 빈도가 낮은 소규모몰에도 통하도록 단순화한 규칙이다. 세그먼트 정의를 바꾸고 싶다는 요청이 오면 `assets/analyze.py`의 `segment()` 함수만 수정한다(SKILL.md의 이 표도 함께 갱신).

## 4단계: 리포트 작성 원칙

1. **핵심 KPI 숫자만 골드(#e8b84b) 포인트, 나머지는 네이비+무채색** - 그라데이션·원형 배지·파스텔 배지·중첩 box-shadow 금지.
2. **확정 수치와 추정 해석을 문장에서 구분한다** - 특이사항 콜아웃은 "확정 근거"(스크립트가 계산한 매출·증감률 그대로)와 "추정 해석"(원인 추측, 예: 시즌·프로모션 여부)을 분리해서 쓴다. 추정 해석은 CSV만으로 확정할 수 없으므로 반드시 "(추정)" 또는 "추정 - " 접두로 표기하고, 확신도 낮은 추측을 단정형 문장으로 쓰지 않는다.
3. **컬럼을 못 찾았거나 계산 불가한 항목은 "산출 불가"로 표기** - 임의 추정치로 채우지 않는다(고객식별자 컬럼 없을 때의 재구매율·RFM이 대표 사례).
4. **표 기반, 화려한 차트 라이브러리 금지** - 막대·수치 비교는 순수 CSS/table로 표현(폭 비율 막대 정도는 허용, JS 차트 라이브러리 금지).
5. **em-dash(가로로 긴 대시 기호) 금지** - 하이픈(-)·가운뎃점(·) 사용, 숫자 중심 개조식 문장.
6. **폰트** `"Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif`.
7. **기간 비교는 2컬럼 그리드**(`grid-template-columns:1fr 1fr`)로 이번 기간·직전 기간을 나란히 배치하고, 증감은 화려한 색상 대신 ▲▼ 기호 + 텍스트로만 표시한다(색상은 KPI 골드 포인트 용도로만 아껴 쓴다).

## 5단계: 검증

- [ ] KPI 칩 5개 수치가 스크립트 출력 `kpi_total`과 정확히 일치
- [ ] 기간 비교 2컬럼의 좌/우가 각각 `period_comparison.previous`/`.current`와 일치
- [ ] RFM 표의 세그먼트별 고객 수 합계 == 고객식별자가 있는 전체 고유 고객 수
- [ ] 특이사항 콜아웃에서 확정 수치(매출·증감률)와 추정 해석이 문장으로 분리되어 있고, 추정 해석에 "(추정)" 표기가 있음
- [ ] 컬럼을 못 찾은 항목이 있으면 "산출 불가"로 명시(임의 수치 없음)
- [ ] em-dash(가로로 긴 대시 기호) 0개
- [ ] 인쇄 시 안내바(`.hint`) 숨김 확인(`@media print`)

## HTML 템플릿 (예시 매출 데이터로 채운 완성 샘플)

아래는 그대로 열어서 확인할 수 있는 완성 샘플이다(가상의 온라인 편집샵 8월 주문 데이터). 실제 작업 시 `assets/analyze.py` 출력값으로 숫자·행 개수를 교체한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>매출 분석 리포트 - 글로우마켓</title>
<style>
  @page { size: A4; margin: 16mm 14mm 16mm 14mm; }
  :root {
    --ink:#1a1a1a; --muted:#555; --line:#cfcfcf; --line2:#888;
    --navy:#1a1a2e; --navy-ink:#ffffff;
    --gold:#e8b84b; --gold-bg:#fbf1dc; --gold-ink:#7a5a12;
  }
  * { box-sizing: border-box; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family:"Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif; color:var(--ink); font-size:10.3pt; line-height:1.6; margin:0; background:#fff; }
  @media screen {
    body { background:#e8e8e8; padding:24px 0; }
    .wrap { max-width:860px; margin:0 auto; background:#fff; padding:40px 46px; box-shadow:0 2px 16px rgba(0,0,0,.18); }
    .hint { max-width:860px; margin:0 auto 14px; background:#fff8e1; border:1px solid #e0c060; padding:10px 16px; font-size:10pt; color:#6a5400; border-radius:4px; }
  }
  @media print { .hint { display:none; } .wrap { padding:0; } }

  .title { text-align:center; font-size:22pt; letter-spacing:10px; font-weight:800; color:var(--navy); margin:0 0 4px; padding-left:10px; }
  .title-sub { text-align:center; font-size:10.5pt; color:var(--muted); margin:0 0 16px; }
  .topline { border-top:3px solid var(--navy); margin:10px 0 18px; }

  .meta { display:flex; justify-content:space-between; font-size:9.7pt; color:var(--muted); border:1px solid var(--line); border-radius:6px; padding:9px 14px; margin-bottom:18px; }
  .meta b { color:var(--ink); }

  h3 { font-size:12pt; border-left:5px solid var(--navy); padding:3px 0 3px 10px; margin:22px 0 8px; }

  /* KPI 칩 */
  .kpi-row { display:grid; grid-template-columns:repeat(5, 1fr); gap:10px; margin:10px 0 6px; }
  .kpi-box { border:1px solid var(--line); border-radius:6px; padding:12px 10px; text-align:center; }
  .kpi-label { font-size:8.6pt; color:var(--muted); margin-bottom:6px; }
  .kpi-value { font-size:15pt; font-weight:900; color:var(--navy); }
  .kpi-value.gold { color:var(--gold-ink); }
  .kpi-unit { font-size:8pt; color:var(--muted); margin-left:2px; font-weight:400; }

  /* 기간 비교 2컬럼 */
  .compare-grid { display:grid; grid-template-columns:1fr 1fr; gap:14px; margin:10px 0 6px; }
  .compare-box { border:1px solid var(--line); border-radius:6px; padding:12px 14px; }
  .compare-box.current { border-color:var(--navy); }
  .compare-box h4 { margin:0 0 8px; font-size:10.3pt; color:var(--navy); border-bottom:1px dashed var(--line); padding-bottom:6px; }
  .compare-row { display:flex; justify-content:space-between; font-size:9.7pt; padding:4px 0; }
  .compare-row .v { font-weight:700; }
  .delta-row { margin-top:8px; padding-top:8px; border-top:1px solid var(--line); font-size:9pt; color:var(--muted); }
  .delta-row b { color:var(--ink); }

  table { width:100%; border-collapse:collapse; margin:6px 0 12px; font-size:9.6pt; table-layout:fixed; }
  th, td { border:1px solid var(--line); padding:7px 8px; vertical-align:top; word-break:break-word; }
  thead th { background:var(--navy); color:var(--navy-ink); font-weight:700; text-align:center; }
  td.num { text-align:right; white-space:nowrap; }
  td.center { text-align:center; }

  .chip { display:inline-block; border-radius:4px; padding:2px 7px; font-size:9.5px; background:var(--gold-bg); border:1px solid var(--gold); color:var(--gold-ink); font-weight:700; }

  .footnote { font-size:9pt; color:var(--muted); margin:6px 0 0; }

  .callout { border-left:4px solid var(--navy); background:#f5f6fa; border-radius:0 5px 5px 0; padding:12px 16px; margin:14px 0 4px; font-size:9.8pt; }
  .callout h4 { margin:0 0 8px; font-size:10.5pt; color:var(--navy); }
  .callout ul { margin:0 0 8px; padding-left:20px; }
  .callout li { margin:3px 0; }
  .callout .estimate { font-style:italic; color:#333; margin:8px 0 0; padding-top:8px; border-top:1px dashed var(--line); }
  .callout .estimate b { font-style:normal; color:var(--navy); }
</style>
</head>
<body>
<div class="hint">📄 인쇄용 매출 분석 리포트입니다. <b>Ctrl/Cmd + P → "PDF로 저장"</b> (배경 그래픽 켜기) 후 사용하세요.</div>
<div class="wrap">

  <div class="title">매출 분석 리포트</div>
  <div class="title-sub">글로우마켓 8월 주문 데이터 분석</div>
  <div class="topline"></div>

  <div class="meta">
    <span><b>분석 대상</b> · 스마트스토어 주문 CSV (2026-08-01 ~ 2026-08-31, 386건)</span>
    <span><b>작성일</b> · 2026-08-31</span>
  </div>

  <h3>1. 핵심 KPI</h3>
  <div class="kpi-row">
    <div class="kpi-box">
      <div class="kpi-label">총매출</div>
      <div class="kpi-value gold">42,850,000<span class="kpi-unit">원</span></div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">총 주문건수</div>
      <div class="kpi-value gold">386<span class="kpi-unit">건</span></div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">평균 주문단가</div>
      <div class="kpi-value gold">111,010<span class="kpi-unit">원</span></div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">재구매율</div>
      <div class="kpi-value gold">34.2<span class="kpi-unit">%</span></div>
    </div>
    <div class="kpi-box">
      <div class="kpi-label">신규 : 재구매 비중</div>
      <div class="kpi-value gold" style="font-size:12.5pt;">61.4 : 38.6<span class="kpi-unit">%</span></div>
    </div>
  </div>
  <p class="footnote">※ 재구매율 = (2회 이상 구매 고객 수 / 전체 고유 고객 수) × 100. 고객식별자(이메일) 컬럼 기준 산출.</p>

  <h3>2. 기간 비교 (이번 기간 vs 직전 기간)</h3>
  <div class="compare-grid">
    <div class="compare-box">
      <h4>직전 기간 (8/1 ~ 8/15)</h4>
      <div class="compare-row"><span>매출</span><span class="v">19,250,000원</span></div>
      <div class="compare-row"><span>주문건수</span><span class="v">172건</span></div>
      <div class="compare-row"><span>평균 주문단가</span><span class="v">111,919원</span></div>
      <div class="compare-row"><span>재구매율</span><span class="v">30.8%</span></div>
    </div>
    <div class="compare-box current">
      <h4>이번 기간 (8/16 ~ 8/31)</h4>
      <div class="compare-row"><span>매출</span><span class="v">23,600,000원</span></div>
      <div class="compare-row"><span>주문건수</span><span class="v">214건</span></div>
      <div class="compare-row"><span>평균 주문단가</span><span class="v">110,280원</span></div>
      <div class="compare-row"><span>재구매율</span><span class="v">36.9%</span></div>
    </div>
  </div>
  <div class="delta-row">
    <b>증감</b> · 매출 ▲22.6% · 주문건수 ▲24.4% · 평균 주문단가 ▼1.5% · 재구매율 ▲6.1%p
  </div>

  <h3>3. RFM 고객 세그먼트</h3>
  <table>
    <colgroup>
      <col style="width:24%"><col style="width:38%"><col style="width:19%"><col style="width:19%">
    </colgroup>
    <thead>
      <tr><th>세그먼트</th><th>정의(R/F/M 기준)</th><th>고객 수</th><th>비중</th></tr>
    </thead>
    <tbody>
      <tr><td>최우수고객</td><td>최근 30일 이내 · 3회 이상 구매 · 구매금액 상위 33%</td><td class="center"><span class="chip">41명</span></td><td class="center">15.3%</td></tr>
      <tr><td>충성고객</td><td>최근성·구매빈도 모두 중간 이상</td><td class="center">58명</td><td class="center">21.6%</td></tr>
      <tr><td>신규고객</td><td>최근 30일 이내 첫 구매(1회)</td><td class="center">72명</td><td class="center">26.9%</td></tr>
      <tr><td>잠재우수</td><td>첫 구매(1회)인데 구매금액 상위 33%</td><td class="center"><span class="chip">19명</span></td><td class="center">7.1%</td></tr>
      <tr><td>이탈위험</td><td>91일 초과 미구매 + 과거 구매빈도·금액 중간 이상</td><td class="center">34명</td><td class="center">12.7%</td></tr>
      <tr><td>휴면/이탈</td><td>91일 초과 미구매 + 구매빈도·금액 모두 하위</td><td class="center">44명</td><td class="center">16.4%</td></tr>
    </tbody>
  </table>
  <p class="footnote">※ 전체 고유 고객 268명 기준. 세그먼트 판정 규칙은 SKILL.md 3단계 우선순위 표 참조.</p>

  <h3>4. 특이사항</h3>
  <div class="callout">
    <h4>상품별 매출 급증/급감</h4>
    <ul>
      <li><b>무드 디퓨저 세트</b> 매출 직전 기간 1,050,000원 → 이번 기간 3,200,000원 (+204.8%, 확정 수치)</li>
      <li><b>여름 린넨 셔츠</b> 매출 직전 기간 2,700,000원 → 이번 기간 1,050,000원 (-61.2%, 확정 수치)</li>
    </ul>
    <p class="estimate"><b>▶ 추정 해석:</b> 무드 디퓨저 세트의 급증 시점이 특정 SNS 인플루언서 협찬 게시물 노출일과 겹치는 것으로 보이나(추정), CSV만으로는 유입 경로를 특정할 수 없어 확정할 수 없다. 여름 린넨 셔츠 급감은 계절 수요 감소로 추정되며(추정), 재고 소진 여부는 별도 확인이 필요하다.</p>
  </div>

</div>
</body>
</html>
```

## 마무리 검증 체크리스트

- [ ] KPI 칩 5개 == 스크립트 출력 `kpi_total`과 일치
- [ ] 기간 비교 좌(직전)/우(이번) 배치와 `period_comparison.previous`/`.current`가 일치
- [ ] RFM 세그먼트별 고객 수 합계 == 고유 고객 수(고객식별자 컬럼이 있을 때만 산출, 없으면 "산출 불가" 명시)
- [ ] 특이사항 콜아웃에 확정 수치(bullet)와 추정 해석(`▶ 추정 해석:`)이 문장으로 분리
- [ ] em-dash(가로로 긴 대시 기호) 0개, 개조식 문장
- [ ] 인쇄 시 `.hint` 안내바 숨김 확인(`@media print`)
