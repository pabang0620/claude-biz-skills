---
name: invoice-organizer
description: 여러 곳에서 흩어져 받은 청구서·영수증(OCR 결과나 수기 입력 등 비정형 텍스트)을 세무사에게 넘기기 전 1차 정리된 매입 기록 표로 만드는 스킬. "청구서 정리해줘", "영수증 뭉치 정리해줘", "매입 내역 표로 만들어줘", "invoice organizer" 요청 시 활성화한다. 발행처·항목·금액·발행일자를 날짜순 표로 정리하고 총 매입액을 강조 바로 표시하는 인쇄(PDF) 최적화 HTML을 생성하며, 발행처별 소계도 옵션으로 지원한다.
version: 1.0.0
triggers:
  - /invoice-organizer
  - 청구서 정리
  - 영수증 정리
---

# invoice-organizer 스킬

## 역할

여러 곳에서 흩어진 상태로 받은 청구서·영수증(카드전표, 세금계산서, 간이영수증, 외주비 청구서 등)을 **1차 정리된 매입 기록 표**로 만든다. 목적은 완결된 세무 신고 자료가 아니라 **세무사에게 넘기기 전 확인 시간을 아끼는 중간 정리물**이다. 입력은 OCR로 뽑은 텍스트든 사용자가 수기로 옮겨 적은 텍스트든 형식이 제각각인 비정형 텍스트로 가정한다.

색상 팔레트(네이비+골드)와 합계 강조 바의 "라벨 작게 + 금액 크게 2단 구성" 레이아웃은 `quote-builder` 스킬의 합계 박스 패턴을 이 스킬의 색상 규칙에 맞게 재구성한 것이다. 다만 그쪽은 좌우 배치(라벨 좌측, 금액 우측)이고 이 스킬은 **위아래 2단 배치**(라벨이 위, 금액이 아래)로 다르다.

## 산출물

- `청구서정리_<기간 또는 용도>_<작성일>.html` (지정 경로 또는 `docs/청구서정리/`)
- 사용자가 크롬에서 `Ctrl+P → PDF로 저장`(배경 그래픽 ON)으로 PDF화

## 입력으로 받을 정보

청구서/영수증 건별로 아래를 원문 텍스트에서 추출한다. 값이 없거나 애매하면 임의로 지어내지 않고 "확인 필요"로 표기해 행 자체는 목록에 남긴다(배제하지 않고 필터링 가능한 상태로 유지).

- 발행처 (필수 - 상호명)
- 항목/품목 (필수 - 세부 품목이 여러 줄이면 대표 품목 요약)
- 금액 (필수 - 실제 지불된 최종 금액)
- 발행일자 (필수 - `YYYY-MM-DD`로 정규화)
- 비고 (결제수단, 증빙 유형, 원천징수 확인 필요 여부 등)

## 텍스트 추출 지침 (형식이 제각각일 때의 처리법)

원문이 카드전표·세금계산서·간이영수증·외주비 청구서 등 형식이 서로 다르므로, 아래 우선순위로 값을 찾는다.

1. **발행처**: "상호", "공급자", "가맹점명" 옆의 값이나 문서 상단 회사명 라인을 우선 채택한다. 개인 프리랜서 외주비처럼 상호가 없으면 사람 이름 그대로 쓴다. 아예 식별이 안 되면 "확인 필요"로 남기고, 다른 건의 발행처를 유추해서 채우지 않는다.
2. **금액**: 한 문서 안에 공급가액·세액·합계금액·결제금액 등 여러 숫자가 섞여 있을 수 있다. **실제 지불된 최종 금액**을 채택하는 순서는 "결제금액" > "합계금액" > "공급가액 + 세액" 순이다. 콤마·"원" 표기는 제거하고 숫자만 남긴다. 어느 숫자를 총액으로 봐야 할지 애매하면 임의로 고르지 말고 비고에 "금액 기준 확인 필요"라고 남긴다.
3. **발행일자**: `2026-08-03`, `2026.08.03`, `26/08/03`, `2026년 8월 3일` 등 표기가 제각각이어도 전부 `YYYY-MM-DD`로 정규화한다. 연도가 생략된 표기(예: `08/03`)는 문서 내 다른 단서(작성 맥락, 파일명 등)로 연도를 추정하되, 추정이면 비고에 "연도 추정"이라고 밝힌다. 추정 근거조차 없으면 연도를 임의로 채우지 말고 "확인 필요"로 둔다.
4. **항목**: 세부 품목이 여러 줄이면 대표 품목 1~2개 + "외 N건"으로 요약한다. 세부 내역 전체가 필요한 작업이면 사용자에게 별도로 확인한다.
5. **비고**: 결제수단(카드/현금/계좌이체), 증빙 유형(세금계산서/현금영수증/간이영수증), 프리랜서 외주비는 "원천징수 3.3% 확인 필요"를 기본으로 남긴다.

## 핵심 원칙

1. **날짜순 정렬** - 발행일자 오름차순(과거 → 최근)으로 정렬한다.
2. **합계 바는 표와 별도 박스** - 표 안의 합계 행이 아니라, quote-builder 패턴을 재구성한 다크 네이비 배경 박스를 표 아래(또는 위)에 독립적으로 둔다. 박스 안은 위아래 2단 구성: "총 매입액" 라벨(작게, 옅은 회색) 위, 금액(크게, 골드 `#e8b84b`, `font-weight:900`) 아래.
3. **골드는 합계금액에만** - 표 헤더·항목·비고 등 다른 곳에 골드나 배지를 쓰지 않는다. 금지: gradient, 원형 배지, 파스텔 배지, 중첩 box-shadow.
4. **표 헤더는 다크 네이비 + 흰 글씨** - `thead th { background:#1a1a2e; color:#ffffff; }`.
5. **발행처별 소계는 옵션** - 기본 산출물은 소계 없는 단일 목록이다. 사용자가 발행처별 소계를 요청하거나 같은 발행처 건이 많아 필요하다고 판단되면, 발행처로 그룹핑한 뒤 그룹 마지막에 `tr.subtotal` 행을 추가한다(아래 "발행처별 소계 옵션" 절 참고). 소계를 켜도 표 전체 정렬 기준(날짜순)은 그룹 내부에서만 유지한다.
6. **합계 검증** - 표에 있는 모든 건의 금액 합 == 합계 바 금액. 소계를 넣었다면 모든 소계의 합 == 합계 바 금액도 함께 검증한다.
7. **고정 안내 문구** - 표 하단에 반드시 "본 표는 1차 정리 자료이며 세무 처리를 위해서는 원본 증빙과 대조가 필요합니다." 문구를 넣는다. 문구를 임의로 바꾸거나 생략하지 않는다.
8. **하이픈 사용** - em대시(-) 금지, 하이픈(-)·가운뎃점(·) 사용. 개조식 문장.

## 생성 절차

1. 원문 텍스트를 건별로 위 "텍스트 추출 지침"에 따라 발행처/항목/금액/발행일자/비고로 1차 정리 - 표로 스스로 정리해본다.
2. 발행일자를 `YYYY-MM-DD`로 정규화하고 오름차순 정렬한다.
3. 발행처별 소계가 필요한지 판단(요청이 있었거나 동일 발행처 건이 3건 이상). 필요하면 발행처로 그룹핑.
4. 금액 합계를 직접 계산해 합계 바에 넣을 총액을 확정한다.
5. 아래 HTML 템플릿의 `<!-- 청구서 행 -->` 반복부를 실제 건수만큼 채운다.
6. 저장 후 표의 행 수 == 입력 건수, 표 금액 합 == 합계 바 금액, 날짜 오름차순 여부를 재검증한다.
7. PDF 변환 안내(크롬 Ctrl+P, 배경 그래픽 ON).

## HTML 템플릿 (예시 청구서 6건으로 채운 완성본)

아래는 그대로 열어서 확인할 수 있는 완성 샘플이다. 실제 작업 시 건수·발행처·항목·금액·날짜만 실제 데이터로 교체한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>청구서 정리 - 2026년 8월 매입 내역</title>
<style>
  @page { size: A4; margin: 16mm 14mm 16mm 14mm; }
  :root {
    --ink:#1a1a1a; --muted:#555; --line:#cfcfcf; --line2:#888;
    --navy:#1a1a2e; --navy-ink:#ffffff;
    --gold:#e8b84b;
  }
  * { box-sizing: border-box; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family:"Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif; color:var(--ink); font-size:10.3pt; line-height:1.6; margin:0; background:#fff; }
  @media screen {
    body { background:#e8e8e8; padding:24px 0; }
    .wrap { max-width:840px; margin:0 auto; background:#fff; padding:40px 46px; box-shadow:0 2px 16px rgba(0,0,0,.18); }
    .hint { max-width:840px; margin:0 auto 14px; background:#fff8e1; border:1px solid #e0c060; padding:10px 16px; font-size:10pt; color:#6a5400; border-radius:4px; }
  }
  @media print { .hint { display:none; } .wrap { padding:0; box-shadow:none; } }

  .title { text-align:center; font-size:22pt; letter-spacing:10px; font-weight:800; color:var(--navy); margin:0 0 4px; padding-left:10px; }
  .title-sub { text-align:center; font-size:10.5pt; color:var(--muted); margin:0 0 16px; }
  .topline { border-top:3px solid var(--navy); margin:10px 0 18px; }

  .meta { display:flex; justify-content:space-between; font-size:9.7pt; color:var(--muted); border:1px solid var(--line); border-radius:6px; padding:9px 14px; margin-bottom:18px; }
  .meta b { color:var(--ink); }

  h3 { font-size:12pt; border-left:5px solid var(--navy); padding:3px 0 3px 10px; margin:20px 0 8px; }

  table { width:100%; border-collapse:collapse; margin:6px 0 14px; font-size:9.6pt; table-layout:fixed; }
  th, td { border:1px solid var(--line); padding:7px 9px; vertical-align:top; word-break:break-word; }
  thead th { background:var(--navy); color:var(--navy-ink); font-weight:700; text-align:center; }
  td.num { text-align:right; white-space:nowrap; }
  td.center { text-align:center; white-space:nowrap; }
  col.c-issuer { width:20%; } col.c-item { width:32%; } col.c-amt { width:14%; } col.c-date { width:13%; } col.c-note { width:21%; }
  tr.subtotal td { background:#eef0f6; font-weight:700; }

  .total-bar { background:var(--navy); border-radius:6px; padding:16px 24px; margin:14px 0 20px; text-align:center; }
  .total-bar .label { display:block; font-size:10pt; color:#b8b8c8; letter-spacing:3px; margin-bottom:6px; }
  .total-bar .amt { display:block; font-size:25pt; font-weight:900; color:var(--gold); }
  .total-bar .amt .unit { font-size:12pt; color:#b8b8c8; font-weight:500; margin-left:6px; }

  .note { background:#f7f7f7; border:1px solid var(--line); border-radius:5px; padding:10px 14px; font-size:9.3pt; margin:10px 0 0; color:var(--muted); }
  .footnote { font-size:9pt; color:var(--muted); margin:6px 0 0; }
</style>
</head>
<body>
<div class="hint">📄 인쇄용 청구서 정리표입니다. <b>Ctrl/Cmd + P → "PDF로 저장"</b> (배경 그래픽 켜기) 후 확인하세요.</div>
<div class="wrap">

  <div class="title">청구서 정리</div>
  <div class="title-sub">2026년 8월 매입 내역 (1차 정리)</div>
  <div class="topline"></div>

  <div class="meta">
    <span><b>정리 대상</b> · 2026년 8월 수취 청구서·영수증 6건</span>
    <span><b>작성일</b> · 2026-08-31</span>
  </div>

  <h3>1. 청구서 목록 (날짜순)</h3>
  <table>
    <colgroup>
      <col class="c-issuer"><col class="c-item"><col class="c-amt"><col class="c-date"><col class="c-note">
    </colgroup>
    <thead>
      <tr><th>발행처</th><th>항목</th><th>금액</th><th>발행일자</th><th>비고</th></tr>
    </thead>
    <tbody>
      <!-- 청구서 행: 실제 건수만큼 반복 -->
      <tr>
        <td>(주)한빛오피스</td>
        <td>사무용품(A4용지 외)</td>
        <td class="num">128,000</td>
        <td class="center">2026-08-03</td>
        <td>카드결제</td>
      </tr>
      <tr>
        <td>스타벅스코리아</td>
        <td>회의용 음료</td>
        <td class="num">42,500</td>
        <td class="center">2026-08-05</td>
        <td>간이영수증</td>
      </tr>
      <tr>
        <td>(주)한빛오피스</td>
        <td>프린터 토너</td>
        <td class="num">215,000</td>
        <td class="center">2026-08-09</td>
        <td>카드결제</td>
      </tr>
      <tr>
        <td>클라우드나인호스팅</td>
        <td>서버 호스팅 이용료(8월분)</td>
        <td class="num">330,000</td>
        <td class="center">2026-08-10</td>
        <td>세금계산서</td>
      </tr>
      <tr>
        <td>김철수 디자인 스튜디오</td>
        <td>로고 리터치 외주비</td>
        <td class="num">500,000</td>
        <td class="center">2026-08-18</td>
        <td>원천징수 3.3% 확인 필요</td>
      </tr>
      <tr>
        <td>클라우드나인호스팅</td>
        <td>도메인 갱신</td>
        <td class="num">33,000</td>
        <td class="center">2026-08-22</td>
        <td>세금계산서</td>
      </tr>
    </tbody>
  </table>
  <p class="footnote">※ 발행일자는 원문 표기(YYYY.MM.DD, YY/MM/DD 등)를 YYYY-MM-DD로 통일한 값입니다.</p>

  <div class="total-bar">
    <span class="label">총 매입액</span>
    <span class="amt">1,248,500<span class="unit">원</span></span>
  </div>

  <p class="note">본 표는 1차 정리 자료이며 세무 처리를 위해서는 원본 증빙과 대조가 필요합니다.</p>

</div>
</body>
</html>
```

## 발행처별 소계 옵션

기본 산출물에는 소계가 없다. 동일 발행처 건이 많아(3건 이상) 발행처별 합계를 같이 보고 싶을 때만 아래처럼 발행처로 그룹핑하고 그룹 마지막 행에 소계를 추가한다. 이때 표 전체 정렬 기준(날짜순)은 그대로 두되, 그룹 내부에서만 발행처가 묶이도록 재배치한다.

```html
<tbody>
  <tr><td>(주)한빛오피스</td><td>사무용품(A4용지 외)</td><td class="num">128,000</td><td class="center">2026-08-03</td><td>카드결제</td></tr>
  <tr><td>(주)한빛오피스</td><td>프린터 토너</td><td class="num">215,000</td><td class="center">2026-08-09</td><td>카드결제</td></tr>
  <tr class="subtotal"><td colspan="2">(주)한빛오피스 소계</td><td class="num">343,000</td><td colspan="2"></td></tr>

  <tr><td>클라우드나인호스팅</td><td>서버 호스팅 이용료(8월분)</td><td class="num">330,000</td><td class="center">2026-08-10</td><td>세금계산서</td></tr>
  <tr><td>클라우드나인호스팅</td><td>도메인 갱신</td><td class="num">33,000</td><td class="center">2026-08-22</td><td>세금계산서</td></tr>
  <tr class="subtotal"><td colspan="2">클라우드나인호스팅 소계</td><td class="num">363,000</td><td colspan="2"></td></tr>
</tbody>
```

소계를 켤 때는 발행처가 1건뿐인 경우(예: 스타벅스코리아, 김철수 디자인 스튜디오)까지 소계 행을 억지로 붙이지 않는다. 모든 소계의 합은 합계 바 금액과 반드시 일치해야 한다(위 예시: 343,000 + 42,500 + 363,000 + 500,000 = 1,248,500).

## 마무리 검증 체크리스트

- [ ] 표의 행 수 == 실제 입력받은 청구서/영수증 건수
- [ ] 발행일자가 전부 `YYYY-MM-DD`로 정규화되어 있고 오름차순 정렬됨
- [ ] 표 안 금액 합 == 합계 바 금액 (소계를 켰다면 소계 합도 동일하게 일치)
- [ ] 발행처·금액·날짜 중 식별 불가 항목은 임의 추정 없이 "확인 필요"로 표기됨
- [ ] 골드(`#e8b84b`)는 합계 바 금액에만 사용, 표·비고에는 미사용
- [ ] 하단에 "본 표는 1차 정리 자료이며 세무 처리를 위해서는 원본 증빙과 대조가 필요합니다." 문구 포함
- [ ] em대시(-) 0개
- [ ] 인쇄 시 `.hint` 안내바 숨김 확인(`@media print`)
