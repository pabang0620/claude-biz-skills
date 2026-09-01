---
name: service-contract-writer
description: 프리랜서/외주 개발자·소상공인이 클라이언트와 맺는 용역계약서를 표준 조항 구조(제1조~제9조+서명란)로 인쇄(PDF) 최적화된 HTML 문서로 즉시 생성하는 스킬. "계약서 써줘", "용역계약서 만들어줘", "외주 계약서 초안", "contract 작성" 같은 요청 시 활성화한다. 조항 구성은 임의로 만든 것이 아니라 실제 통용되는 프리랜서 용역계약서 표준 양식(위임인/수임인, 제1조~제9조)을 그대로 따른다.
version: 1.1.0
triggers:
  - /service-contract-writer
  - 용역계약서
  - 계약서
---

# service-contract-writer 스킬

## 역할
갑(발주자, 위임인)/을(수급자, 수임인) 정보와 용역 조건을 받아 **표준 프리랜서 용역계약 양식**을 A4 인쇄(PDF) 최적화 HTML로 생성한다.
사용자(을, 공급자)는 보통 **개인 프리랜서 개발자 또는 소상공인**이며, 상대방(갑)은 발주 기업·기관인 경우가 많다.

이 스킬은 조항을 새로 창작하지 않는다. 제1조~제9조 구성과 조항별 문구는 실제 통용되는 프리랜서 위임계약서 표준 양식을 그대로 따르고, HTML/CSS 레이아웃만 인쇄 최적화 형태로 입힌다.

## 산출물
- `용역계약서_<프로젝트 또는 용역명>_<을>.html` (지정 경로 또는 `docs/계약서/`)
- 사용자가 크롬에서 `Ctrl+P → PDF로 저장`(배경 그래픽 ON)으로 PDF화, 또는 인쇄 후 자필 서명·날인

## 입력으로 받을 정보 (없으면 질문하거나 기본값 적용)
- **갑(발주자, 위임인)**: 상호, 대표자, 주소
- **을(수급자, 수임인)**: 성명, 주민등록번호(선택 - 을이 개인정보 기재를 원하지 않으면 공란 처리 가능하다고 안내), 주소, 연락처
- **용역명·업무 내용**: 을이 수행할 업무를 호별로 나열
- **계약기간**: 착수일 ~ 종료일
- **대금**: 계약금액(부가세 포함 여부), 선금(금액·지급시점), 잔금(금액·지급시점)
- **잔금 지급 기한**: 검수완료 후 며칠 이내인지 (기본값 있으면 적용)

## 기본값 규칙 (정보가 없을 때)
- **선금/잔금 비율**: 사용자가 지정하지 않으면 선금 30% / 잔금 70%를 제안하고, 채택 여부를 사용자에게 알린 뒤 진행한다.
- **잔금 지급 기한**: 검수완료 후 기한을 지정하지 않으면 "검수완료 후 7일 이내"를 제안한다.
- **성과물 권리 귀속**: 별도 약정이 없는 한 업무 결과물의 소유권 및 지식재산권은 "갑"에게 귀속된다 (표준 양식 그대로 - 조건부 이전 등 임의 조항을 추가하지 않는다).
- 위 기본값은 모두 **채택 여부를 사용자에게 알리고** 진행한다 - 조용히 채워 넣고 넘어가지 않는다.

## 표준 조항 구조
제1조(계약의 목적) · 제2조(계약기간) · 제3조(업무 내용) · 제4조(대금) · 제5조(대금 지급 방법) · 제6조(권리) · 제7조(비밀유지) · 제8조(계약 해지) · 제9조(기타) · 서명란(위임인/수임인)

## 스타일 원칙
- 폰트: `"Batang","바탕","Malgun Gothic","맑은 고딕","Noto Sans KR",serif` (공식 계약서류는 바탕체)
- 색상: 메인 네이비 `#0d2137`, 텍스트 `#111`, 배경 흰색. 포인트색 없음(격식 문서는 강조색 최소화)
- 표 헤더: 네이비 배경 + 흰 글씨 + 중앙정렬
- A4 인쇄 최적화: `@page { size:A4; }`, 화면에서만 box-shadow, `@media print`에서 제거
- 서명란: 실선 박스/표, "(인)" 문구, `page-break-inside:avoid`
- 절대 쓰지 말 것: gradient, `border-radius:50%`, 파스텔 pill 배지, 여러 곳 중첩 box-shadow
- 개조식/짧은 문장, em-dash 금지(하이픈 사용)

## 생성 절차
1. 입력 정보 확인 (부족하면 질문).
2. 기본값을 적용할 항목(선금/잔금 비율·잔금 지급기한)이 있으면 어떤 기본값을 썼는지 사용자에게 알린다.
3. 대금 내역: 선금+잔금 합계가 총 계약금액과 정확히 일치하는지 검산.
4. 아래 HTML 템플릿의 `{{...}}` 자리를 실제 값으로 치환 (업무 내용은 호 개수만큼 `<li>` 반복).
5. 파일 저장 후 미치환 `{{` 잔존 여부를 grep으로 확인.
6. PDF 변환 안내 (크롬 Ctrl+P, 배경 그래픽 ON) 또는 인쇄 후 서명·날인 안내.

## HTML 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>용역계약서 - {{용역명}}</title>
<style>
  @page { size: A4; margin: 16mm 18mm 16mm 18mm; }
  * { box-sizing: border-box; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { font-family:"Batang","바탕","Malgun Gothic","맑은 고딕","Noto Sans KR",serif; color:#111; font-size:10.5pt; line-height:1.68; margin:0; background:#fff; }
  @media screen { body{ background:#d8d8d8; padding:30px 0;} .wrap{ max-width:800px; margin:0 auto; background:#fff; padding:52px 58px; box-shadow:0 4px 24px rgba(0,0,0,.18);} .hint{max-width:800px;margin:0 auto 14px;background:#e8f4fd;border:1px solid #90caf9;padding:10px 16px;font-size:9.5pt;color:#1a4a7a;} }
  @media print { .hint{display:none;} .wrap{padding:0;} }

  .doc-title-wrap { text-align:center; margin-bottom:28px; }
  .doc-title { font-size:23pt; font-weight:900; letter-spacing:14px; color:#0d2137; margin:0 0 5px; padding-left:14px; }
  .doc-title-line { width:80px; height:3px; background:#0d2137; margin:12px auto 0; }

  .preamble { font-size:10.5pt; margin:0 0 22px; text-align:center; }

  h3.clause { font-size:11.5pt; font-weight:800; color:#0d2137; margin:20px 0 8px; padding-bottom:4px; border-bottom:1.5px solid #0d2137; font-family:"Malgun Gothic","맑은 고딕",sans-serif; }
  .clause p { margin:5px 0; }
  .clause ul.list { margin:6px 0 6px 1.2em; padding:0; }
  .clause ul.list li { margin:3px 0; }

  table.pay-table { width:100%; border-collapse:collapse; margin:6px 0 4px; font-family:"Malgun Gothic","맑은 고딕",sans-serif; font-size:9.7pt; }
  .pay-table thead th { background:#0d2137; color:#fff; text-align:center; padding:7px 9px; border:1px solid #0d2137; font-weight:700; }
  .pay-table td { border:1px solid #c8d4df; padding:6px 9px; text-align:center; }
  .pay-table td.left { text-align:left; }
  .pay-table tr.total td { font-weight:800; background:#eef3f8; }

  .sign-area { margin-top:30px; page-break-inside:avoid; break-inside:avoid; }
  .sign-date { text-align:center; font-size:10.5pt; margin-bottom:20px; letter-spacing:2px; }
  table.sign-table { width:100%; border-collapse:collapse; font-family:"Malgun Gothic","맑은 고딕",sans-serif; font-size:10pt; }
  .sign-table th { background:#0d2137; color:#fff; text-align:center; padding:8px 0; width:50%; font-weight:700; }
  .sign-table td { border:1px solid #c8d4df; padding:16px 18px; vertical-align:top; line-height:2.1; }
  .sign-table .k { display:inline-block; width:5.4em; color:#333; }
  .sign-table .seal { color:#888; font-size:9pt; }
</style>
</head>
<body>
<div class="hint">📄 인쇄용 용역계약서입니다. <b>Ctrl/Cmd + P → "PDF로 저장"</b>(배경 그래픽 ON) 후 사용하거나, 인쇄하여 서명·날인하세요.</div>
<div class="wrap">

  <div class="doc-title-wrap">
    <div class="doc-title">용 역 계 약 서</div>
    <div class="doc-title-line"></div>
  </div>

  <p class="preamble">
    {{갑상호}}(이하 "갑")와(과) {{을성명}}(이하 "을")은 신의 성실의 원칙에 따라<br>
    다음과 같이 계약을 체결한다.
  </p>

  <div class="clause">
    <h3 class="clause">제1조(계약의 목적)</h3>
    <p>본 계약은 {{용역명 또는 계약목적 내용}}을 목적으로 한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제2조(계약기간)</h3>
    <p>본 계약 기간은 {{착수일}}부터 {{종료일}}까지로 한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제3조(업무 내용)</h3>
    <p>"을"은 다음 각 호의 업무를 수행한다.</p>
    <ul class="list">
      <li>{{업무1}}</li>
      <li>{{업무2}}</li>
      <li>{{업무3}}</li>
    </ul>
  </div>

  <div class="clause">
    <h3 class="clause">제4조(대금)</h3>
    <p>1. 계약금액: {{총금액}}원(VAT 포함)</p>
    <table class="pay-table">
      <thead>
        <tr><th style="width:22%">구분</th><th style="width:38%">지급 시점</th><th style="width:40%">금액</th></tr>
      </thead>
      <tbody>
        <tr><td class="left">2. 선금</td><td>{{선금 지급시점}}</td><td>{{선금액}}원</td></tr>
        <tr><td class="left">3. 잔금</td><td>{{잔금 지급시점}}</td><td>{{잔금액}}원</td></tr>
        <tr class="total"><td colspan="2">합계</td><td>{{총금액}}원</td></tr>
      </tbody>
    </table>
  </div>

  <div class="clause">
    <h3 class="clause">제5조(대금 지급 방법)</h3>
    <p>1. "갑"은 제4조에서 정한 대금을 "을" 명의의 계좌로 지급한다.</p>
    <p>2. "갑"은 검수완료 후 {{잔금 지급기한, 기본 7}}일 이내에 잔금을 지급한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제6조(권리)</h3>
    <p>별도의 약정이 없는 경우 업무 결과물에 대한 소유권 및 지적재산권은 "갑"에게 귀속된다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제7조(비밀유지)</h3>
    <p>"을"은 업무 수행 중 취득한 정보를 외부에 누설하거나 업무 목적 외로 사용할 수 없다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제8조(계약 해지)</h3>
    <p>다음 각 호의 경우 계약을 해지할 수 있다.</p>
    <ul class="list">
      <li>"을"이 계약상 의무를 위반한 경우</li>
      <li>부득이한 사정으로 업무 수행이 불가한 경우</li>
      <li>기타 상호 합의에 의한 경우</li>
    </ul>
  </div>

  <div class="clause">
    <h3 class="clause">제9조(기타)</h3>
    <p>본 계약서에 명시되지 않은 사항은 당사자 간 협의에 따라 결정한다.</p>
  </div>

  <div class="sign-area">
    <div class="sign-date">{{계약일자, 연 월 일}}</div>
    <table class="sign-table">
      <tr><th>위임인 (갑)</th><th>수임인 (을)</th></tr>
      <tr>
        <td>
          <span class="k">상&nbsp;&nbsp;호</span>: {{갑상호}}<br>
          <span class="k">대표자</span>: {{갑대표자}} <span class="seal">(인)</span><br>
          <span class="k">주&nbsp;&nbsp;소</span>: {{갑주소}}
        </td>
        <td>
          <span class="k">성&nbsp;&nbsp;명</span>: {{을성명}} <span class="seal">(인)</span><br>
          <span class="k">주민번호</span>: {{을주민번호, 선택 - 공란 가능}}<br>
          <span class="k">주&nbsp;&nbsp;소</span>: {{을주소}}<br>
          <span class="k">연락처</span>: {{을연락처}}
        </td>
      </tr>
    </table>
  </div>

</div>
</body>
</html>
```

## 마무리 검증 체크리스트
- [ ] 대금 내역: 선금+잔금 합 == 총 계약금액 (제4조①, 표 합계 행 2곳)
- [ ] 갑/을 정보가 본문(전문·서명란) 2곳에서 모두 동일하게 일치
- [ ] 조 번호 1~9 연속·중복 없음, 서명란 누락 없음
- [ ] em대시(-) 0개
- [ ] 미치환 `{{` 잔존 0개
