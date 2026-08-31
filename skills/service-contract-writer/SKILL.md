---
name: service-contract-writer
description: 프리랜서/외주 개발자·소상공인이 클라이언트와 맺는 용역계약서를 표준 조항 구조(제1조~제10조+부칙+서명란)로 인쇄(PDF) 최적화된 HTML 문서로 즉시 생성하는 스킬. "계약서 써줘", "용역계약서 만들어줘", "외주 계약서 초안", "contract 작성" 같은 요청 시 활성화한다. 갑/을 정보·용역 범위·계약금액·지급방법·특약사항을 입력받아 성과물 귀속 시점·비밀유지·해지·손해배상·관할법원까지 포함한 정식 계약서 양식을 채운다.
version: 1.0.0
triggers:
  - /service-contract-writer
  - 용역계약서
  - 계약서
---

# service-contract-writer 스킬

## 역할
갑(발주자)/을(수급자) 정보와 용역 조건을 받아 **한국 프리랜서·소상공인 용역계약 관례에 맞는 정식 계약서**를 A4 인쇄(PDF) 최적화 HTML로 생성한다.
사용자(을, 공급자)는 보통 **개인 프리랜서 개발자 또는 소상공인**이며, 상대방(갑)은 발주 기업·기관인 경우가 많다.

## 산출물
- `용역계약서_<프로젝트 또는 용역명>_<을>.html` (지정 경로 또는 `docs/계약서/`)
- 사용자가 크롬에서 `Ctrl+P → PDF로 저장`(배경 그래픽 ON)으로 PDF화, 또는 인쇄 후 자필 서명·날인

## 입력으로 받을 정보 (없으면 질문하거나 기본값 적용)
- **갑(발주자)**: 상호/성명, 주소, 대표자, 사업자등록번호(있으면)
- **을(수급자)**: 상호/성명, 주소, 대표자 또는 본인 성명, 사업자등록번호(있으면 - 없으면 "개인(비사업자)"로 표기)
- **용역 범위·내용**: 무엇을 만드는지/무엇을 하는지 목록
- **계약기간**: 착수일 ~ 완료일
- **계약금액 및 지급방법**: 총액, 계약금/중도금/잔금 비율(없으면 기본값 제안)
- **특약사항**: 있으면 목록, 없으면 "해당 없음"으로 기재

## 기본값 규칙 (정보가 없을 때)
- **지급 방법**: 계약금(착수 시) 30% / 잔금(검수·완료 시) 70%. 금액 규모가 크거나 사용자가 중도금을 원하면 계약금 30% / 중도금 30% / 잔금 40%로 3분할 제안.
- **비사업자 원천징수**: "을"이 개인(비사업자)이면 제4조에 사업소득세 3.3% 원천징수 문구를 자동 포함. "을"이 사업자(과세)면 해당 문구를 빼고 세금계산서 발행 문구로 대체.
- **지식재산권 귀속 시점**: 계약금액 **전액 지급 완료 시점**에 갑에게 이전 (관례상 표준 - 잔금 미지급 상태에서 성과물 권리가 넘어가는 구조는 을에게 불리하므로 채택하지 않는다).
- **비밀유지 존속기간**: 계약 종료 후 2년.
- **해지 시정기간**: 시정 요구 후 7일.
- **관할법원**: "을"의 주소지를 관할하는 법원 (본 스킬의 주 사용자가 을 = 프리랜서/소상공인이므로 기본값을 을에게 유리한 쪽으로 둔다. 갑 쪽에서 이의가 있으면 사용자가 직접 조정).
- 위 기본값은 모두 **채택 여부를 사용자에게 알리고** 진행한다 - 조용히 채워 넣고 넘어가지 않는다.

## 표준 조항 구조
제1조(목적) · 제2조(계약기간) · 제3조(용역의 범위) · 제4조(계약금액 및 지급방법) · 제5조(성과물의 귀속) · 제6조(비밀유지) · 제7조(계약의 변경 및 해지) · 제8조(손해배상) · 제9조(분쟁해결) · 제10조(특약사항) · 부칙 · 서명란(갑/을)

## 스타일 원칙
- 폰트: `"Batang","바탕","Malgun Gothic","맑은 고딕","Noto Sans KR",serif` (공식 계약서류는 바탕체)
- 색상: 메인 네이비 `#0d2137`, 텍스트 `#111`, 배경 흰색. 포인트색 없음(격식 문서는 강조색 최소화)
- 표 헤더: 네이비 배경 + 흰 글씨 + 중앙정렬
- A4 인쇄 최적화: `@page { size:A4; }`, 화면에서만 box-shadow, `@media print`에서 제거
- 서명란: 실선 박스/표, "(서명 또는 인)" 문구, `page-break-inside:avoid`
- 절대 쓰지 말 것: gradient, `border-radius:50%`, 파스텔 pill 배지, 여러 곳 중첩 box-shadow
- 개조식/짧은 문장, em-dash 금지(하이픈 사용)

## 생성 절차
1. 입력 정보 확인 (부족하면 질문). "을"의 사업자 여부는 반드시 확인 - 원천징수 문구 갈림.
2. 기본값을 적용할 항목(지급비율·귀속시점·비밀유지기간·관할법원 등)이 있으면 어떤 기본값을 썼는지 사용자에게 알린다.
3. 지급 내역 표: 계약금+중도금+잔금 합계가 총액과 정확히 일치하는지 검산.
4. 아래 HTML 템플릿의 `{{...}}` 자리를 실제 값으로 치환 (용역 범위·특약사항은 목록 항목 수만큼 `<li>` 반복).
5. 파일 저장 후 옛값·미치환 `{{` 잔존 여부를 grep으로 확인.
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
  body { font-family:"Batang","바탕","Malgun Gothic","맑은 고딕","Noto Sans KR",serif; color:#111; font-size:10.5pt; line-height:1.62; margin:0; background:#fff; }
  @media screen { body{ background:#d8d8d8; padding:30px 0;} .wrap{ max-width:800px; margin:0 auto; background:#fff; padding:52px 58px; box-shadow:0 4px 24px rgba(0,0,0,.18);} .hint{max-width:800px;margin:0 auto 14px;background:#e8f4fd;border:1px solid #90caf9;padding:10px 16px;font-size:9.5pt;color:#1a4a7a;} }
  @media print { .hint{display:none;} .wrap{padding:0;} }

  /* 헤더 */
  .doc-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:22px; font-family:"Malgun Gothic","맑은 고딕",sans-serif; }
  .doc-no { font-size:9pt; color:#888; text-align:right; }

  /* 제목 */
  .doc-title-wrap { text-align:center; margin-bottom:26px; }
  .doc-title { font-size:23pt; font-weight:900; letter-spacing:14px; color:#0d2137; margin:0 0 5px; padding-left:14px; }
  .doc-title-en { font-family:"Malgun Gothic","맑은 고딕",sans-serif; font-size:9pt; letter-spacing:3px; color:#7a9ab8; margin:0 0 14px; text-transform:uppercase; }
  .doc-title-line { width:80px; height:3px; background:#0d2137; margin:0 auto; }

  .preamble { font-size:10.5pt; margin:0 0 18px; text-align:center; }

  /* 갑/을 정보 표 */
  .info-table { width:100%; border-collapse:collapse; margin-bottom:20px; font-family:"Malgun Gothic","맑은 고딕",sans-serif; }
  .info-table th { background:#0d2137; color:#fff; font-size:9.5pt; font-weight:700; text-align:center; padding:7px 10px; border:1px solid #0d2137; width:16%; }
  .info-table td { font-size:9.5pt; padding:7px 12px; border:1px solid #c8d4df; background:#fff; }

  /* 조항 */
  h3.clause { font-size:11.5pt; font-weight:800; color:#0d2137; margin:20px 0 8px; padding-bottom:4px; border-bottom:1.5px solid #0d2137; }
  .clause p { margin:5px 0; }
  .clause ul.scope-list { margin:6px 0 6px 1.2em; padding:0; }
  .clause ul.scope-list li { margin:3px 0; }

  /* 지급 내역 표 */
  table.pay-table { width:100%; border-collapse:collapse; margin:8px 0 6px; font-family:"Malgun Gothic","맑은 고딕",sans-serif; font-size:9.7pt; }
  .pay-table thead th { background:#0d2137; color:#fff; text-align:center; padding:7px 9px; border:1px solid #0d2137; font-weight:700; }
  .pay-table td { border:1px solid #c8d4df; padding:6px 9px; text-align:center; }
  .pay-table td.left { text-align:left; }
  .pay-table tr.total td { font-weight:800; background:#eef3f8; }

  .small { font-size:9pt; color:#555; font-family:"Malgun Gothic","맑은 고딕",sans-serif; }

  /* 부칙 */
  .bujeok { margin-top:22px; font-size:10pt; text-align:center; }

  /* 서명 */
  .sign-area { margin-top:26px; page-break-inside:avoid; break-inside:avoid; }
  .sign-date { text-align:center; font-size:10.5pt; margin-bottom:18px; letter-spacing:2px; }
  .sign-row { display:flex; gap:24px; }
  .sign-box { flex:1; border:1px solid #555; padding:14px 18px; }
  .sign-box h4 { margin:0 0 10px; font-size:10.5pt; font-family:"Malgun Gothic","맑은 고딕",sans-serif; background:#0d2137; color:#fff; text-align:center; padding:6px 0; }
  .sign-box .ln { margin:8px 0; font-size:10pt; }
  .sign-box .k { display:inline-block; width:5.4em; color:#333; }
  .sign-box .seal { float:right; color:#888; font-size:9pt; font-family:"Malgun Gothic","맑은 고딕",sans-serif; }
</style>
</head>
<body>
<div class="hint">📄 인쇄용 용역계약서입니다. <b>Ctrl/Cmd + P → "PDF로 저장"</b>(배경 그래픽 ON) 후 사용하거나, 인쇄하여 서명·날인하세요.</div>
<div class="wrap">

  <div class="doc-header">
    <div class="doc-no">문서번호 : {{문서번호, 없으면 생략}}</div>
    <div class="doc-no">작성일 : {{작성일}}</div>
  </div>

  <div class="doc-title-wrap">
    <div class="doc-title">용 역 계 약 서</div>
    <div class="doc-title-en">Service Agreement</div>
    <div class="doc-title-line"></div>
  </div>

  <p class="preamble">
    {{갑상호}}(이하 "갑"이라 한다)와(과) {{을상호}}(이하 "을"이라 한다)는<br>
    {{용역명}}에 관하여 다음과 같이 용역계약을 체결한다.
  </p>

  <table class="info-table">
    <tr>
      <th>구분</th><th>갑 (발주자)</th><th>을 (수급자)</th>
    </tr>
    <tr>
      <th>상호/성명</th><td>{{갑상호}}</td><td>{{을상호}}</td>
    </tr>
    <tr>
      <th>대표자</th><td>{{갑대표자}}</td><td>{{을대표자 또는 본인}}</td>
    </tr>
    <tr>
      <th>주소</th><td>{{갑주소}}</td><td>{{을주소}}</td>
    </tr>
    <tr>
      <th>사업자등록번호</th><td>{{갑사업자번호, 없으면 "-"}}</td><td>{{을사업자번호, 없으면 "개인(비사업자)"}}</td>
    </tr>
  </table>

  <div class="clause">
    <h3 class="clause">제1조(목적)</h3>
    <p>본 계약은 "갑"이 "을"에게 {{용역명}} 관련 용역을 의뢰하고, "을"이 이를 성실히 수행함에 있어 필요한 제반 사항을 정함을 목적으로 한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제2조(계약기간)</h3>
    <p>① 본 계약에 따른 용역 수행 기간은 {{착수일}}부터 {{완료일}}까지로 한다.</p>
    <p>② 천재지변, "갑"의 요청에 따른 용역 범위 변경 등 부득이한 사유가 발생하는 경우 "갑"과 "을"은 협의하여 기간을 조정할 수 있다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제3조(용역의 범위)</h3>
    <p>① "을"이 수행하는 용역의 범위는 다음과 같다.</p>
    <ul class="scope-list">
      <li>{{용역범위 항목1}}</li>
      <li>{{용역범위 항목2}}</li>
      <li>{{용역범위 항목3}}</li>
    </ul>
    <p>② 제1항에 포함되지 않는 추가 작업은 "갑"과 "을"이 별도로 협의하여 추가 계약 또는 서면 합의를 통해 진행한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제4조(계약금액 및 지급방법)</h3>
    <p>① 본 용역의 총 계약금액은 금 {{금액한글}}원(₩{{금액숫자}})으로 한다.</p>
    <p>② 대금은 다음과 같이 분할하여 지급한다.</p>
    <table class="pay-table">
      <thead>
        <tr><th style="width:22%">구분</th><th style="width:30%">지급 시기</th><th style="width:18%">비율</th><th style="width:30%">금액</th></tr>
      </thead>
      <tbody>
        <tr><td class="left">계약금</td><td>계약 체결 시</td><td>{{계약금비율}}%</td><td>₩{{계약금액}}</td></tr>
        <!-- 중도금 있을 때만 -->
        <tr><td class="left">중도금</td><td>{{중도금 지급 시기}}</td><td>{{중도금비율}}%</td><td>₩{{중도금액}}</td></tr>
        <tr><td class="left">잔금</td><td>검수·완료 시</td><td>{{잔금비율}}%</td><td>₩{{잔금액}}</td></tr>
        <tr class="total"><td colspan="3">합계</td><td>₩{{금액숫자}}</td></tr>
      </tbody>
    </table>
    <p class="small">③ "을"이 개인(비사업자)인 경우 "갑"은 대금 지급 시 소득세법에 따른 사업소득세 3.3%를 원천징수한 후 지급할 수 있다. (실지급액 = 각 회차 금액 × 0.967, 세전/실수령 기준은 협의)</p>
    <p>④ 대금은 "을"이 지정하는 계좌로 입금하는 방식으로 지급한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제5조(성과물의 귀속)</h3>
    <p>① 본 용역의 결과로 발생하는 성과물(소스코드, 디자인, 문서 등 일체)에 대한 지식재산권은 "갑"이 "을"에게 제4조의 계약금액 전액을 지급 완료한 시점에 "갑"에게 귀속된다.</p>
    <p>② 대금 지급이 완료되기 전까지 성과물에 대한 저작권 등 지식재산권은 "을"에게 있다.</p>
    <p>③ "을"이 본 용역 수행 과정에서 사용한 "을"의 기존 라이브러리, 프레임워크, 사전 보유 기술(오픈소스 포함)에 대한 권리는 "을"에게 유보되며, "갑"은 본 용역의 목적 범위 내에서 이를 이용할 수 있다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제6조(비밀유지)</h3>
    <p>① "갑"과 "을"은 본 계약의 수행 과정에서 알게 된 상대방의 영업비밀 및 기술정보를 상대방의 서면 동의 없이 제3자에게 누설하거나 본 계약 목적 외의 용도로 사용하지 아니한다.</p>
    <p>② 본 조의 비밀유지 의무는 계약 종료 후에도 {{비밀유지기간, 기본 2}}년간 유효하다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제7조(계약의 변경 및 해지)</h3>
    <p>① 본 계약의 내용을 변경하고자 할 경우 "갑"과 "을"은 서면 합의를 통해 변경할 수 있다.</p>
    <p>② 다음 각 호의 어느 하나에 해당하는 경우, 상대방에게 서면으로 통지한 후 계약을 해지할 수 있다.</p>
    <ul class="scope-list">
      <li>상대방이 본 계약상 의무를 중대하게 위반하고, 시정을 요구받은 날로부터 {{시정기간, 기본 7}}일 이내에 이를 시정하지 아니한 경우</li>
      <li>상대방에게 파산, 회생절차 개시 등 계약 이행이 곤란한 사유가 발생한 경우</li>
    </ul>
    <p>③ 계약이 해지되는 경우 "을"은 해지 시점까지 수행한 용역에 상당하는 대금을 "갑"에게 청구할 수 있으며, "갑"은 이를 정산하여 지급한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제8조(손해배상)</h3>
    <p>"갑" 또는 "을"이 본 계약을 위반하여 상대방에게 손해를 입힌 경우, 귀책 당사자는 상대방에게 발생한 손해를 배상한다. 다만 천재지변 등 불가항력적 사유로 인한 손해에 대하여는 그러하지 아니하다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제9조(분쟁해결)</h3>
    <p>① 본 계약과 관련하여 발생하는 분쟁은 "갑"과 "을"이 상호 협의하여 원만히 해결함을 원칙으로 한다.</p>
    <p>② 협의가 이루어지지 아니할 경우, 본 계약과 관련한 소송의 관할법원은 {{관할법원, 기본 "을"의 주소지를 관할하는 법원}}으로 한다.</p>
  </div>

  <div class="clause">
    <h3 class="clause">제10조(특약사항)</h3>
    <p>{{특약사항, 없으면 "해당 없음"}}</p>
  </div>

  <p class="bujeok">
    <b>부칙</b><br>
    본 계약을 증명하기 위하여 계약서 2부를 작성하고, "갑"과 "을"이 각각 서명 또는 날인한 후 각 1부씩 보관한다.
  </p>

  <div class="sign-area">
    <div class="sign-date">{{계약일자, 연 월 일}}</div>
    <div class="sign-row">
      <div class="sign-box">
        <h4>갑 (발주자)</h4>
        <div class="ln"><span class="k">상&nbsp;&nbsp;호</span> {{갑상호}}</div>
        <div class="ln"><span class="k">주&nbsp;&nbsp;소</span> {{갑주소}}</div>
        <div class="ln"><span class="k">대 표 자</span> {{갑대표자}} <span class="seal">(서명 또는 인)</span></div>
      </div>
      <div class="sign-box">
        <h4>을 (수급자)</h4>
        <div class="ln"><span class="k">상&nbsp;&nbsp;호</span> {{을상호}}</div>
        <div class="ln"><span class="k">주&nbsp;&nbsp;소</span> {{을주소}}</div>
        <div class="ln"><span class="k">대 표 자</span> {{을대표자 또는 본인}} <span class="seal">(서명 또는 인)</span></div>
      </div>
    </div>
  </div>

</div>
</body>
</html>
```

## 사업자(과세) "을" 버전 차이
- 제4조 ③항 원천징수 문구(개인(비사업자) 대상) 제거
- 대신 "을"은 대금 수령 시 세금계산서(또는 계산서)를 발행한다는 문구로 대체
- info-table의 을 "사업자등록번호"란에 실제 번호 기재

## 마무리 검증 체크리스트
- [ ] 지급 내역 표: 계약금+중도금(있으면)+잔금 합 == 총 계약금액 (2곳: 제4조①, 합계 행)
- [ ] 갑/을 정보가 본문(전문·정보표·서명란) 3곳에서 모두 동일하게 일치
- [ ] "을" 사업자 여부에 따라 원천징수 문구 포함/제거 정확
- [ ] 조 번호 1~10 연속·중복 없음, 부칙·서명란 누락 없음
- [ ] em대시(-) 0개
- [ ] 미치환 `{{` 잔존 0개
