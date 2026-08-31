---
name: quote-comparison
description: 여러 업체(벤더)에서 받은 견적서·제안서를 하나의 비교표로 정리해 최적 선택을 돕는 스킬. "견적 비교해줘", "업체별 견적서 비교표 만들어줘", "이 견적서들 정리해줘", "vendor comparison", "quote comparison" 같은 요청 시 활성화한다. 인쇄(PDF) 최적화 HTML 비교표를 생성하며, 업체 2~5곳까지 동적으로 대응하고, 최저가·유리 조건 강조와 근거 구분된 결론 콜아웃을 포함한다.
version: 1.0.0
triggers:
  - /quote-comparison
  - 견적 비교
---

# quote-comparison 스킬

## 역할

2곳 이상 업체(벤더)로부터 받은 견적서/제안서를 **하나의 비교표**로 정리해, 의사결정자가 가격뿐 아니라 납기·특이조건까지 한눈에 보고 선택할 수 있게 돕는다. A4 인쇄(PDF) 최적화 HTML로 산출하며, 단순 최저가 나열이 아니라 **"확정된 사실"과 "판단자의 재량 판단"을 문장에서 명확히 구분**한 결론을 함께 제시한다.

`quote-builder`(견적서 작성)와 같은 계열이며 색상 팔레트·인쇄 스타일 컨벤션(`@page A4`, 화면 전용 인쇄 안내바, `@media screen/print` 분기)을 그대로 따른다. 차이는 단일 견적서가 아니라 **다업체 비교표**라는 점, 그리고 팔레트가 네이비+골드 포인트라는 점이다.

## 산출물

- `견적비교_<프로젝트명>_<작성일>.html` (지정 경로 또는 `docs/견적비교/`)
- 사용자가 크롬에서 `Ctrl+P → PDF로 저장`(배경 그래픽 ON)으로 PDF화

## 입력으로 받을 정보 (없으면 질문하거나 "미기재"로 표기)

업체(벤더)별로 다음을 받는다. 텍스트, PDF 추출 텍스트, 이미지 설명(사용자가 옮겨 적어준 값) 등 형태는 무관하다.

- 업체명 (필수)
- 항목별 세부 가격 (있는 만큼 - 업체마다 항목 구성이 다를 수 있음)
- 총액 (필수 - 없으면 항목 합으로 계산하고 "항목 합산" 표기)
- 납기
- 특이조건: 하자보수기간, 유지보수 포함 여부, 결제조건 등
- 평점/신뢰도(있으면 - 없으면 행 자체를 생략)

## 핵심 원칙

1. **비교 목적/기준일을 상단에 명시** - "무엇을 위한 비교인지"(예: 사무실 인테리어 시공 3사 비교)와 작성일을 반드시 적는다. 기준일이 없으면 오늘 날짜로 채우지 말고 사용자에게 확인한다.
2. **표는 항목(행) × 업체(열)** - 첫 열은 항목명 고정, 나머지 열은 업체 수만큼 동적으로 늘어난다. 업체가 2곳이면 2열, 5곳이면 5열.
3. **행 없는 정보는 임의로 만들지 않는다** - 특정 업체가 특이조건을 안 적었으면 "미기재"로 표기한다. 다른 업체 값을 유추해서 채우지 않는다(filter 원칙 - 없는 값은 없는 채로 보여주고 사용자가 판단하게 한다).
4. **최저가/유리 조건은 chip으로 소극적으로 강조** - 골드(#e8b84b) 계열의 작은 텍스트 chip(`border-radius:4px 이하, padding:3px 8px, font-size:11.5px`)만 쓴다. 과장된 원형 배지·그라데이션·큰 뱃지 금지.
5. **결론은 사실과 판단을 구분해서 쓴다**
   - **확정 근거**: 표에서 그대로 읽히는 사실. 예) "가격은 A사가 최저(1,200만원)."
   - **판단자의 재량 판단**: 여러 조건을 종합한 추천. 예) "다만 하자보수기간은 B사가 6개월 더 길어, 총 비용 대비 유지보수 리스크를 고려하면 B사도 검토할 만하다."
   - 두 문장을 시각적으로도 구분한다(사실은 일반체, 판단은 `▶ 종합 판단:` 접두어 + 이탤릭).
   - 단정적 결론("A사로 결정")을 스킬이 대신 내리지 않는다. 근거를 정리해서 제시하고 최종 선택은 사용자 몫으로 남긴다.
6. **업체 수가 유동적** - 2~5곳을 기본 지원. 6곳 이상이면 가로 스크롤 대신 사용자에게 표를 두 그룹으로 나눌지 확인한다(A4 폭 초과 방지).
7. **하이픈 사용** - em대시(-) 금지, 하이픈(-)·가운뎃점(·) 사용. 개조식 문장.
8. **합계 검증** - 항목별 가격 합이 표시된 총액과 다르면(부가세·할인 등으로 다를 수 있음) "항목 합산과 총액 차이"를 각주로 남긴다. 조용히 넘어가지 않는다.

## 생성 절차

1. 업체별 입력 정보를 정리 - 업체명, 항목별 가격, 총액, 납기, 특이조건, 평점(있으면)을 표로 먼저 스스로 정리해본다.
2. 업체 수(n)를 확인 - 아래 템플릿의 `<th>`/`<td>`를 n개로 맞춰 반복 생성한다. 표 폭 계산: 첫 열(항목명) 22%, 나머지 열은 `(100-22)/n`%씩 균등 배분. n=2면 39%씩, n=5면 15.6%씩.
3. 항목별 세부 가격표(1개 이상 행) + 요약 구간(총액/납기/특이조건/평점) 순서로 작성.
4. 업체별 최저가 셀, 조건상 유리한 셀에 `<span class="chip">` 적용. 어느 기준으로 "유리"라 판단했는지 애매하면(예: 납기가 짧은 게 항상 유리한지 여부) chip을 달지 않고 표만 보여준다.
5. 결론 콜아웃 작성 - 확정 근거 bullet 2~3개 + 종합 판단 1~2문장.
6. 파일 저장 후, 항목 합산 vs 총액 불일치·업체 수와 열 개수 일치·chip 적용 근거를 grep/육안으로 재검증.
7. PDF 변환 안내(크롬 Ctrl+P, 배경 그래픽 ON).

## HTML 템플릿 (4개 업체 예시로 채운 완성본)

아래는 그대로 열어서 확인할 수 있는 완성 샘플이다. 실제 작업 시 업체 수·항목·값만 교체한다(2곳이면 열 2개만 남기고, 5곳이면 열 1개를 더 추가).

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>견적 비교표 - 사무실 인테리어 시공</title>
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

  h3 { font-size:12pt; border-left:5px solid var(--navy); padding:3px 0 3px 10px; margin:20px 0 8px; }

  table { width:100%; border-collapse:collapse; margin:6px 0 12px; font-size:9.6pt; table-layout:fixed; }
  th, td { border:1px solid var(--line); padding:7px 8px; vertical-align:top; word-break:break-word; }
  thead th { background:var(--navy); color:var(--navy-ink); font-weight:700; text-align:center; }
  td.num { text-align:right; white-space:nowrap; }
  td.center { text-align:center; }
  tr.total td { font-weight:800; background:#f0f0f5; font-size:10.3pt; }
  .item-col { width:22%; font-weight:600; }
  .vendor-col { width:19.5%; }

  .chip { display:inline-block; border-radius:4px; padding:3px 8px; font-size:11.5px; background:var(--gold-bg); border:1px solid var(--gold); color:var(--gold-ink); font-weight:700; }

  .footnote { font-size:9pt; color:var(--muted); margin:6px 0 0; }

  .conclusion { border-left:4px solid var(--navy); background:#f5f6fa; border-radius:0 5px 5px 0; padding:12px 16px; margin:16px 0 4px; font-size:9.8pt; }
  .conclusion h4 { margin:0 0 8px; font-size:10.5pt; color:var(--navy); }
  .conclusion ul { margin:0 0 8px; padding-left:20px; }
  .conclusion li { margin:3px 0; }
  .conclusion .judgment { font-style:italic; color:#333; margin:8px 0 0; padding-top:8px; border-top:1px dashed var(--line); }
  .conclusion .judgment b { font-style:normal; color:var(--navy); }
</style>
</head>
<body>
<div class="hint">📄 인쇄용 견적 비교표입니다. <b>Ctrl/Cmd + P → "PDF로 저장"</b> (배경 그래픽 켜기) 후 사용하세요.</div>
<div class="wrap">

  <div class="title">견적 비교표</div>
  <div class="title-sub">사무실 인테리어 시공 견적 비교 (4개사)</div>
  <div class="topline"></div>

  <div class="meta">
    <span><b>비교 목적</b> · 신규 사무실(가양동, 33평) 인테리어 시공 업체 선정</span>
    <span><b>기준일</b> · 2026-08-31</span>
  </div>

  <h3>1. 항목별 세부 가격</h3>
  <table>
    <colgroup>
      <col class="item-col"><col class="vendor-col"><col class="vendor-col"><col class="vendor-col"><col class="vendor-col">
    </colgroup>
    <thead>
      <tr><th>항목</th><th>A사</th><th>B사</th><th>C사</th><th>D사</th></tr>
    </thead>
    <tbody>
      <tr><td class="item-col">철거·기초공사</td><td class="num">3,200,000</td><td class="num">3,000,000</td><td class="num">3,500,000</td><td class="num">2,900,000</td></tr>
      <tr><td class="item-col">전기·조명</td><td class="num">2,800,000</td><td class="num">3,100,000</td><td class="num">2,600,000</td><td class="num">3,300,000</td></tr>
      <tr><td class="item-col">바닥·마감재</td><td class="num">4,500,000</td><td class="num">4,200,000</td><td class="num">4,800,000</td><td class="num">4,000,000</td></tr>
      <tr><td class="item-col">가구·집기</td><td class="num">1,500,000</td><td class="num">1,700,000</td><td class="num">1,400,000</td><td class="num">1,800,000</td></tr>
      <tr class="total">
        <td class="item-col">합계</td>
        <td class="num"><span class="chip">12,000,000</span></td>
        <td class="num">12,000,000</td>
        <td class="num">12,300,000</td>
        <td class="num">12,000,000</td>
      </tr>
    </tbody>
  </table>
  <p class="footnote">※ A사·D사는 항목 합산과 견적서 총액이 동일. B사·C사도 확인 결과 일치. 부가세 별도 여부는 업체별 계약서 재확인 필요.</p>

  <h3>2. 조건 비교</h3>
  <table>
    <colgroup>
      <col class="item-col"><col class="vendor-col"><col class="vendor-col"><col class="vendor-col"><col class="vendor-col">
    </colgroup>
    <thead>
      <tr><th>항목</th><th>A사</th><th>B사</th><th>C사</th><th>D사</th></tr>
    </thead>
    <tbody>
      <tr>
        <td class="item-col">총액</td>
        <td class="num"><span class="chip">1,200만원</span></td>
        <td class="num">1,200만원</td>
        <td class="num">1,230만원</td>
        <td class="num"><span class="chip">1,200만원</span></td>
      </tr>
      <tr>
        <td class="item-col">납기</td>
        <td class="center">18일</td>
        <td class="center"><span class="chip">14일</span></td>
        <td class="center">21일</td>
        <td class="center">20일</td>
      </tr>
      <tr>
        <td class="item-col">하자보수기간</td>
        <td class="center">6개월</td>
        <td class="center"><span class="chip">12개월</span></td>
        <td class="center">6개월</td>
        <td class="center">미기재</td>
      </tr>
      <tr>
        <td class="item-col">유지보수 포함</td>
        <td class="center">미포함</td>
        <td class="center"><span class="chip">1년 무상</span></td>
        <td class="center">미포함</td>
        <td class="center">미기재</td>
      </tr>
      <tr>
        <td class="item-col">평점/실적</td>
        <td class="center">시공 실적 40건</td>
        <td class="center">시공 실적 25건</td>
        <td class="center">시공 실적 60건</td>
        <td class="center">미기재</td>
      </tr>
    </tbody>
  </table>

  <div class="conclusion">
    <h4>결론</h4>
    <ul>
      <li>총액은 A사·B사·D사가 1,200만원으로 동일 최저, C사가 300만원(약 2.5%) 높음.</li>
      <li>납기는 B사가 14일로 가장 짧고(A사 대비 4일 단축), 하자보수기간도 B사만 12개월(타사 대비 2배).</li>
      <li>D사는 하자보수기간·유지보수 포함 여부가 견적서에 미기재 - 계약 전 반드시 확인 필요.</li>
    </ul>
    <p class="judgment"><b>▶ 종합 판단:</b> 가격만 보면 A/B/D사가 동률 최저지만, 납기와 하자보수 조건까지 종합하면 <b>B사</b>가 가장 유리한 조건으로 판단됨. 다만 이는 가격 외 조건에 가중치를 둔 판단이며, 가격 단일 기준이면 A/B/D사 중 아무 곳이나 동일 조건이다. D사는 특이조건 미기재분을 확인하기 전까지는 비교 대상에서 완전히 제외하지 않되 판단 보류가 맞다.</p>
  </div>

</div>
</body>
</html>
```

## 마무리 검증 체크리스트

- [ ] 표의 업체 열 개수 == 실제 입력받은 업체 수
- [ ] 항목별 가격 합 == 표시된 총액(다르면 각주로 명시, 조용히 넘기지 않음)
- [ ] chip은 "최저가" 또는 "조건상 유리"에만 적용, 근거 없는 chip 없음
- [ ] 미기재 항목은 "미기재"로 표기, 임의 추정 값 없음
- [ ] 결론에서 확정 근거(bullet)와 종합 판단(`▶ 종합 판단:`)이 문장으로 분리되어 있음
- [ ] em대시(-) 0개
- [ ] 인쇄 시 `.hint` 안내바 숨김 확인(`@media print`)
