---
name: resume-screener
description: 지원자 이력서 여러 건을 채용공고 요구조건 기준 비교표로 정리하는 스킬. HR 담당자 없이 채용을 직접 진행하는 소상공인·1인사업자가 지원자 검토 시간을 줄이도록 돕는다. "지원자 이력서 비교해줘", "채용 스크리닝 해줘", "이력서 검토표 만들어줘", "지원자들 정리해줘" 요청 시 활성화한다. 합격/불합격 판정이나 적합도 점수·추천 여부는 절대 산출하지 않으며, 채용공고 요구조건 대비 지원자가 기재한 정보를 사실 그대로 병기하는 대조표만 만든다(자동화된 채용 판정은 법적 리스크가 있다).
version: 1.0.0
triggers:
  - 지원자 이력서 비교해줘
  - 채용 스크리닝 해줘
  - 이력서 검토표 만들어줘
---

# resume-screener 스킬

## ⚠️ 매우 중요한 제약 (예외 없이 준수)

**이 스킬은 "합격/불합격 판정"을 절대 하지 않는다.** 자동화된 도구가 채용 여부를 판단하거나 그렇게 읽힐 수 있는 산출물을 만드는 것은 법적 리스크(채용절차법 등 관련 규제, 차별 소지)가 있다.

- 산출물에 다음 어휘를 **절대 쓰지 않는다**: "적합", "부적합", "추천", "비추천", "합격 가능성", "우수", "미흡", "통과", "탈락", pass/fail 류 표현 일체.
- 산출물에 판단성 색상 강조를 **절대 쓰지 않는다**: 빨강/초록 신호등, 골드·그린 계열 "좋음" 뉘앙스 포인트색, 원형 점수 배지 등.
- 이 스킬이 만드는 것은 오직 **"채용공고에 명시된 요구조건" vs "지원자가 제출한 정보"를 있는 그대로 병기하는 대조표**뿐이다. 예: "요구 경력 3년 이상" / "지원자 기재 경력 2년" 처럼 사실을 나란히 적을 뿐, 그 둘을 비교해 충족 여부를 최종 판정("충족"/"미충족" 같은 이분법 표기 포함)하지 않는다.
- 지원서에 없는 내용을 추론·과장·완곡화하지 않는다. 기재가 없으면 "미기재"로 표기한다.
- 채용 여부는 **전적으로 사용자(고용주)가 표를 보고 직접 판단**한다. 산출물 하단에 이 사실을 알리는 안내 문구를 항상 고정 포함한다(아래 템플릿 참조).

## 역할

채용공고 요구조건(직무·경력·필수스킬·우대사항·희망연봉대 등)과 지원자 여러 명의 이력서(텍스트로 추출된 것)를 입력받아, 지원자별로 요구조건 대비 기재 정보를 나열한 비교표를 A4/화면 겸용 HTML로 만든다. 목적은 "지원자 10명의 이력서를 일일이 다시 훑지 않아도 항목별로 빠르게 훑어볼 수 있게" 정리하는 것이지, 누구를 뽑을지 대신 정해주는 것이 아니다.

## 산출물

- `이력서비교_<채용포지션>_<작성일>.html` (지정 경로 없으면 `docs/채용/` 또는 사용자가 지정한 위치)
- 화면에서 바로 훑어볼 수 있고, 필요하면 크롬에서 `Ctrl+P → PDF로 저장`으로도 출력 가능하게 인쇄 스타일 포함

## 입력으로 받을 정보 (부족하면 질문)

- **채용공고 요구조건**: 직무명, 요구 경력연수, 필수 스킬/자격, 우대사항, 희망연봉대(공고 제시 범위), 근무형태(정규직/계약직 등), 마감일
- **지원자 이력서**: 여러 건, 텍스트로 추출된 상태(파일을 그대로 첨부·붙여넣기). PDF/HWP 자체 파싱은 이 스킬 범위가 아니다 - 이미 텍스트화된 내용을 입력으로 받는다.
- 지원자 수가 많으면(10명 이상) 사용자에게 전부 한 표에 넣을지, 채용공고 필수 요건만으로 1차 표를 나눌지 확인한다(1차 표도 판정이 아니라 항목 나열임을 유지).

## 핵심 원칙

1. **병기 원칙** - 모든 비교 항목은 열 머리글에 "요구조건"을 작게 표기하고, 셀에는 "지원자 기재" 사실만 넣는다. 요구조건과 지원자 기재를 한 셀 안에서 최종 판정 기호(O/X, 충족/미충족)로 압축하지 않는다.
2. **사실만, 추론 금지** - 이력서에 없는 내용을 채워 넣지 않는다. 없으면 "미기재". 애매한 표현("다수의 프로젝트 경험")은 이력서 원문 표현을 그대로 옮기고 임의로 구체화하지 않는다.
3. **색상은 중립 회색조만** - 표 헤더는 다크네이비(`#1a1a2e`) + 흰 글씨로 통일. 셀 강조가 필요해도 옅은 회색(`#f4f4f6`) 줄무늬 정도만 쓰고, 골드·그린 등 "좋음" 뉘앙스 포인트색은 이 스킬에서 원칙적으로 쓰지 않는다.
4. **건조체·개조식** - 사실 나열 위주로 짧게 쓴다. 지원동기 요약도 지원자의 원문 취지를 요약할 뿐 평가하지 않는다("열정적이다", "적극적이다" 같은 평가어 금지, 지원자가 직접 쓴 표현만 인용/축약).
5. **하단 고정 안내 문구 필수** - "이 표는 지원서에 기재된 정보를 기계적으로 정리한 것이며 채용 판단을 대신하지 않습니다"를 산출물 하단에 항상 포함한다. 생략 금지.
6. **em-dash 금지** - 하이픈(-)을 쓴다.
7. **개인정보 취급 주의** - 주민등록번호, 사진, 가족관계 등 채용 항목과 무관한 민감정보는 표에 옮기지 않는다(비교표는 직무 관련 항목만 다룬다).

## 생성 절차

1. 채용공고 요구조건을 확인하고 정리한다(부족하면 질문). 요구조건 항목이 비교표 열이 된다.
2. 지원자 이력서 각각에서 해당 항목의 정보만 사실 그대로 추출한다. 추론·보완 금지, 없으면 "미기재".
3. 아래 HTML 템플릿의 상단 요구조건 요약과 비교표를 채운다. 지원자 행 × 요구조건 열 구조를 유지한다.
4. 하단 고정 안내 문구가 누락되지 않았는지 확인한다.
5. 최종 점검 - 아래 "마무리 검증 체크리스트"의 금지 어휘·금지 색상이 산출물에 하나도 없는지 grep 수준으로 재확인한다.

## HTML 템플릿

예시 지원자 3명(경력 미달/경력 초과/스킬 일부 상이 등 다양한 케이스) 데이터로 채운 완성 샘플이다. 실제 사용 시 `<!-- 지원자 행 반복 -->` 부분을 지원자 수만큼 늘리고 내용을 교체한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>지원자 이력서 비교표 - 백엔드 개발자</title>
<style>
  @page { size: A4 landscape; margin: 14mm 12mm; }
  :root {
    --ink:#1a1a1a; --muted:#5a5a5a; --line:#d8d8d8; --line2:#9a9a9a;
    --navy:#1a1a2e; --navy-ink:#ffffff; --zebra:#f4f4f6; --req:#7a7a7a;
  }
  * { box-sizing: border-box; }
  html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body {
    font-family:"Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    color:var(--ink); font-size:10.3pt; line-height:1.55; margin:0; background:#fff;
  }
  @media screen {
    body { background:#e9e9ec; padding:24px 0; }
    .wrap { max-width:1180px; margin:0 auto; background:#fff; padding:36px 40px; box-shadow:0 2px 14px rgba(0,0,0,.15); }
  }
  @media print { .wrap { padding:0; } }

  .title { font-size:20pt; font-weight:800; color:var(--navy); margin:0 0 4px; }
  .title-sub { font-size:10.5pt; color:var(--muted); margin:0 0 14px; }
  .topline { border-top:3px solid var(--navy); margin:8px 0 16px; }

  h3 { font-size:11.5pt; color:var(--navy); border-left:5px solid var(--navy); padding:2px 0 2px 10px; margin:20px 0 8px; }

  .req-box { border:1px solid var(--line); border-radius:6px; padding:12px 16px; margin-bottom:14px; background:#fafafb; }
  .req-box table { width:100%; border:none; }
  .req-box td { border:none; padding:3px 0; font-size:9.8pt; vertical-align:top; }
  .req-box td.k { color:var(--muted); width:110px; font-weight:700; }

  table.compare { width:100%; border-collapse:collapse; margin:8px 0 6px; font-size:9.3pt; }
  table.compare th, table.compare td { border:1px solid var(--line); padding:8px 9px; vertical-align:top; text-align:left; }
  table.compare thead th { background:var(--navy); color:var(--navy-ink); font-weight:700; text-align:center; }
  table.compare thead th .req { display:block; font-weight:400; font-size:8.3pt; color:#cfd0dd; margin-top:3px; }
  table.compare tbody tr:nth-child(even) { background:var(--zebra); }
  table.compare td.name { font-weight:700; white-space:nowrap; text-align:center; }
  table.compare td.fact { color:var(--ink); }
  table.compare td.empty { color:#a0a0a0; font-style:italic; }

  .notice {
    margin-top:18px; padding:12px 16px; border:1px solid var(--line2); border-radius:6px;
    background:#f7f7f8; font-size:9.5pt; color:var(--ink); font-weight:700; text-align:center;
  }
  .footnote { margin-top:8px; font-size:8.8pt; color:var(--muted); }
</style>
</head>
<body>
<div class="wrap">

  <div class="title">지원자 이력서 비교표</div>
  <div class="title-sub">백엔드 개발자 채용 · 작성일 2026-08-31</div>
  <div class="topline"></div>

  <h3>1. 채용공고 요구조건 (참조용)</h3>
  <div class="req-box">
    <table>
      <tr><td class="k">직무</td><td>백엔드 개발자 (Node.js/Express)</td></tr>
      <tr><td class="k">요구 경력</td><td>3년 이상</td></tr>
      <tr><td class="k">필수 스킬</td><td>Node.js, Express, MySQL</td></tr>
      <tr><td class="k">우대사항</td><td>AWS 운영 경험, TypeScript</td></tr>
      <tr><td class="k">학력</td><td>무관</td></tr>
      <tr><td class="k">공고 제시 연봉</td><td>3,500만원 ~ 4,200만원</td></tr>
      <tr><td class="k">근무형태</td><td>정규직 (수습 3개월)</td></tr>
    </table>
  </div>

  <h3>2. 지원자 대조표</h3>
  <table class="compare">
    <thead>
      <tr>
        <th style="width:9%">지원자</th>
        <th style="width:14%">경력연수<span class="req">요구: 3년 이상</span></th>
        <th style="width:20%">보유 스킬<span class="req">요구: Node.js·Express·MySQL 필수 / AWS·TS 우대</span></th>
        <th style="width:12%">학력<span class="req">요구: 무관</span></th>
        <th style="width:13%">희망연봉<span class="req">공고 제시: 3,500~4,200만원</span></th>
        <th style="width:32%">지원동기 (지원자 원문 요약)</th>
      </tr>
    </thead>
    <tbody>
      <!-- 지원자 행 반복: 실제 사용 시 지원자 수만큼 늘릴 것 -->
      <tr>
        <td class="name">김OO</td>
        <td class="fact">지원자 기재: 2년</td>
        <td class="fact">기재: Node.js, Express, MySQL, React</td>
        <td class="fact">4년제 컴퓨터공학과 졸업</td>
        <td class="fact">지원자 기재: 3,800만원</td>
        <td class="fact">"작은 팀에서 프론트-백엔드를 함께 다뤄본 경험을 살려 서비스 전체 흐름에 기여하고 싶다"고 기재</td>
      </tr>
      <tr>
        <td class="name">이OO</td>
        <td class="fact">지원자 기재: 5년</td>
        <td class="fact">기재: Node.js, Express, MySQL, AWS(EC2/RDS), TypeScript</td>
        <td class="fact">전문학사 (정보통신과)</td>
        <td class="fact">지원자 기재: 4,500만원 (희망, 협의 가능이라고 기재)</td>
        <td class="fact">"이전 회사에서 인프라 이관을 주도한 경험을 이어가고 싶다"고 기재</td>
      </tr>
      <tr>
        <td class="name">박OO</td>
        <td class="fact">지원자 기재: 1년</td>
        <td class="fact">기재: Node.js, Express / MySQL 기재 없음(스터디 경험만 언급)</td>
        <td class="fact">4년제 산업공학과 졸업</td>
        <td class="empty">미기재</td>
        <td class="fact">"신입 개발자로 실무 경험을 쌓고 싶다"고 기재</td>
      </tr>
    </tbody>
  </table>

  <div class="notice">이 표는 지원서에 기재된 정보를 기계적으로 정리한 것이며 채용 판단을 대신하지 않습니다.</div>
  <p class="footnote">※ "요구조건"란은 채용공고 원문 기준이며, "지원자 기재"란은 지원자가 이력서/지원서에 직접 작성한 내용을 그대로 옮긴 것입니다. 기재가 없는 항목은 "미기재"로 표시했습니다. 최종 채용 여부는 작성자(고용주)가 직접 판단합니다.</p>

</div>
</body>
</html>
```

## 마무리 검증 체크리스트

- [ ] "적합", "부적합", "추천", "비추천", "합격 가능성", "우수", "미흡", "통과", "탈락" 등 판정 어휘 0건
- [ ] 빨강/초록 신호등 색상, 골드·그린 "좋음" 강조색, 원형 점수 배지 0건 (표 헤더는 다크네이비 `#1a1a2e` + 흰 글씨만)
- [ ] 셀에 O/X, 충족/미충족 같은 판정 기호 0건 (요구조건과 지원자 기재를 병기만 했는지 확인)
- [ ] 하단 고정 안내 문구("이 표는 ... 채용 판단을 대신하지 않습니다") 포함 여부
- [ ] em-dash(—) 0개, 하이픈(-) 사용
- [ ] 이력서에 없는 내용을 추론해 채운 셀이 없는지 (없으면 "미기재"로 되어 있는지)
- [ ] 주민등록번호·사진·가족관계 등 직무 무관 민감정보가 표에 옮겨지지 않았는지
