---
name: cs-inquiry-triage
description: 일정 기간 쌓인 고객 문의(이메일/채팅/게시판 문의 뭉치, 형식이 일정하지 않은 텍스트 로그나 CSV 포함)를 사람이 하나씩 읽지 않고도 이슈 유형별로 자동 집계해 반복되는 문제와 사업 개선점을 파악하게 한다. "고객문의 정리해줘", "CS 티켓 집계해줘", "문의 유형별로 나눠줘", "문의 뭉치 분석해줘" 같은 요청 시 활성화한다.
version: 1.0.0
triggers:
  - /cs-inquiry-triage
  - CS 문의 집계
  - 고객문의 정리
---

# cs-inquiry-triage 스킬

## 역할

일정 기간 쌓인 고객 문의(이메일 export, 채팅 로그, 게시판 문의 게시글, CSV 등)를 받아 **사람이 한 건씩 읽지 않아도 되도록** 이슈 유형별로 자동 분류·집계하고, 반복되는 문제와 그 문제가 시사하는 사업 개선점을 화면 조회용 HTML 리포트로 만든다.

이 스킬은 개별 문의 티켓을 처리(답변 작성·배정)하는 도구가 아니다. **이미 쌓인 문의 더미를 사후적으로 훑어 패턴을 읽어내는** 집계·분석 도구다.

## 산출물

- `CS문의집계_<기간>.html` (지정 경로 또는 사용자가 요청한 위치)
- 화면에서 바로 조회하는 용도. 인쇄가 필요하면 브라우저 인쇄 기능을 그대로 쓰면 되므로 `@page`/A4 인쇄 스타일은 필수로 넣지 않는다(넣더라도 선택 사항으로만 취급).
- 저장 전, 대상 경로에 동일 파일명이 이미 있으면 자동으로 덮어쓰지 않고 사용자에게 먼저 알린다.

## 입력으로 받을 정보

- 문의 뭉치 원본: 다음 형태 중 무엇이든 가능하다.
  - CSV/엑셀 export (헤더 있음/없음 모두 가능)
  - 이메일을 그대로 복붙한 텍스트 (날짜·제목·본문이 뒤섞인 형태)
  - 채팅/카카오톡 로그 (타임스탬프 + 발화자 + 메시지 반복)
  - 게시판 문의글 목록 (제목+본문+작성일 나열)
- 집계 대상 기간(선택): 사용자가 명시하지 않으면 데이터에서 관측되는 최초~최종 날짜를 그대로 쓰고 리포트 상단에 명시한다.
- 채널 구분(선택): 이메일/채팅/게시판/전화 등. 데이터에 명시가 없으면 "채널 미상"으로 둔다. 채널별 집계가 필수 요구사항은 아니며, 유형별 집계가 핵심이다.

## 핵심 원칙

1. **유형은 고정 목록이 아니라 데이터를 보고 그때그때 정한다.** "배송지연", "결제오류" 같은 카테고리를 미리 강제하지 않는다. 실제 문의 내용을 읽고 자연스럽게 묶이는 이슈 유형을 Claude가 스스로 명명한다.
2. **유형 개수는 통상 5~8개 내외로 수렴시킨다.** 문의량이 아주 적으면(10건 이하) 더 적어도 되고, 아주 많으면 조금 늘어나도 된다. 다만 유형을 지나치게 잘게 쪼개면(예: "배송지연", "배송지연(주말)", "배송지연(해외)"을 별도 유형으로) 집계의 의미가 사라지므로 상위 개념으로 묶는다. 나머지 소수 건은 "기타"로 모은다.
3. **원문은 임의로 재해석하지 않는다.** 대표 문의 예시는 고객이 실제로 쓴 문장을 요약하되, 없는 맥락을 지어 붙이지 않는다. 문장이 길면 핵심만 남기고 줄이는 정도로 그친다.
4. **추측은 추측이라고 표시한다.** "이 유형이 왜 반복되는가"에 대한 원인 분석은 데이터만으로 확정할 수 없는 경우가 대부분이다. 이런 문장은 반드시 "~로 보인다", "~일 가능성이 있다" 식으로 추정임을 명시하고, 확정형 단정("~때문이다", "~이 원인이다")을 쓰지 않는다.
5. **비중이 큰 유형만 콜아웃으로 강조한다.** 전체 문의 중 비중이 가장 크거나(대략 20% 이상 또는 최다 1~2개 유형) 압도적으로 반복되는 유형만 별도로 강조 표시한다. 나머지는 평범한 섹션으로 나열한다. 강조를 남발하면 강조가 무의미해진다.
6. **하이픈 사용.** em대시(—) 금지, 하이픈(-) 사용. 화살표(→)·가운뎃점(·)은 허용.
7. **건조한 보고체.** "~확인됨", "~로 집계됨", "~로 보임" 같은 개조식·보고체를 쓴다. 카피라이팅식 감탄사·이모지·느낌표 남발 금지.

## 처리 절차

### 1단계: 문의 뭉치 파싱

입력 형식이 일정하지 않다는 것을 전제로 유연하게 처리한다.

- **CSV/엑셀**: 헤더가 있으면 날짜/채널/내용에 해당하는 컬럼을 이름으로 매칭한다(예: `date`, `문의일`, `등록일` 등은 날짜로, `channel`, `구분` 등은 채널로, `content`, `내용`, `문의내용`, `제목+본문` 등은 본문으로). 헤더가 없으면 값의 패턴(날짜 형식, 텍스트 길이)으로 열 역할을 추정한다.
- **텍스트 로그(이메일/채팅 복붙)**: 줄바꿈 2회 이상, 또는 날짜/시간 패턴(`YYYY-MM-DD`, `MM/DD`, `오전/오후 HH:MM` 등)이 반복 등장하는 지점을 문의 단위 구분자로 삼는다. 구분이 애매하면 빈 줄 기준으로 1차 분리 후, 너무 길게 묶인 덩어리는 내부 날짜 패턴으로 재분리한다.
- **채널 판별**: 본문이나 메타데이터에 "카카오", "채팅", "메일", "게시판", "전화" 등의 단서가 있으면 그것을 채널로 쓴다. 단서가 전혀 없으면 "채널 미상"으로 두고 억지로 추정하지 않는다.
- **파싱이 애매한 건**: 문의로 보기 어려운 잡음(서명, 광고, 시스템 자동 발신 등)은 건수에서 제외하고, 제외한 건수와 사유를 리포트 하단에 한 줄로 밝힌다.
- **건수가 아주 많을 때(수백 건 이상)**: 전수를 한 번에 다 인용하지 않는다. 유형별 대표 예시 2~3건만 뽑고, 나머지는 건수 집계에만 반영한다.

### 2단계: 유형 분류

- 문의 본문을 읽고 무엇을 요구/불만/질문하는지 파악해 유형을 부여한다.
- 유형명은 명사형으로 짧게(예: "배송 지연", "결제 오류", "환불 절차 문의", "상품 정보 문의", "로그인/계정 문제").
- 한 문의가 여러 이슈를 동시에 담고 있으면(예: 배송 지연 + 환불 요청) 더 핵심적인 요구사항 쪽 유형 하나로 분류한다. 억지로 다중 카운트하지 않는다.
- 유형별 정렬은 건수 내림차순으로 한다.

### 3단계: 대표 예시·공통 패턴 요약

- 유형별로 대표 문의 2~3개를 골라 원문 요약을 인용한다.
- 각 유형 아래에 공통 패턴 한 줄 요약을 덧붙인다(예: "특정 택배사 경유 건에 집중되는 경향이 있음").

### 4단계: 반복 빈도 판정 및 콜아웃

- 전체 대비 비중이 크게 도드라지는 유형(대략 20% 이상 또는 1~2위 유형)만 콜아웃 박스로 별도 강조한다.
- 콜아웃에는 반드시 "이 유형이 반복되면 근본 원인(제품/프로세스) 점검이 필요하다"는 식의 실행 시사점을 한 줄 포함한다. 이 문장도 추정이면 추정 표현을 쓴다.

### 5단계: 저장 및 검증

- HTML 템플릿에 실데이터를 채워 저장한다.
- 저장 전 다음을 재계산해 확인한다.
  - 유형별 건수 합 == 총 문의 건수(제외 처리한 잡음 건수는 별도 명시)
  - 상단 chip에 표기한 건수와 본문 섹션의 건수가 일치하는지
  - 콜아웃으로 강조한 유형이 실제로 비중 기준(대략 20% 이상 또는 최다 1~2개)을 충족하는지
- 동일 파일명이 이미 있으면 덮어쓰지 않고 사용자에게 먼저 알린다.

## HTML 템플릿 (예시 데이터로 채운 샘플)

아래는 실제 산출물의 완전한 예시다. 새로 만들 때는 이 구조·CSS를 그대로 쓰고 데이터만 실제 집계 결과로 치환한다. 유형 개수·콜아웃 개수는 실데이터에 맞게 늘리거나 줄인다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CS 문의 집계 리포트</title>
<style>
  :root {
    --navy: #1a1a2e;
    --muted: #555;
    --line: #d8d8dc;
    --line2: #9a9aa4;
    --bg: #fff;
    --bg-soft: #f6f6f9;
    --alert: #a13030;
    --alert-bg: #fbf1f1;
  }
  * { box-sizing: border-box; }
  body {
    font-family: "Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    color: var(--navy);
    font-size: 14px;
    line-height: 1.65;
    margin: 0;
    background: var(--bg-soft);
  }
  .wrap {
    max-width: 880px;
    margin: 0 auto;
    background: var(--bg);
    padding: 40px 44px 60px;
  }
  @media (max-width: 600px) {
    .wrap { padding: 24px 18px 40px; }
  }
  header.title-block {
    border-bottom: 3px solid var(--navy);
    padding-bottom: 16px;
    margin-bottom: 20px;
  }
  h1 {
    font-size: 22px;
    margin: 0 0 6px;
    color: var(--navy);
  }
  .meta {
    font-size: 12.5px;
    color: var(--muted);
  }

  /* 요약 chip */
  .chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 18px 0 28px;
  }
  .chip {
    border: 1px solid var(--line2);
    background: var(--bg-soft);
    padding: 6px 12px;
    font-size: 12.5px;
    color: var(--navy);
  }
  .chip b { font-weight: 700; }
  .chip.total {
    border-color: var(--navy);
    background: var(--navy);
    color: #fff;
  }

  /* 유형별 섹션 */
  section.type-section {
    border-top: 1px solid var(--line);
    padding: 20px 0;
  }
  section.type-section:last-of-type {
    border-bottom: 1px solid var(--line);
  }
  .type-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .type-head h2 {
    font-size: 16px;
    margin: 0;
    color: var(--navy);
  }
  .type-head .count {
    font-size: 12.5px;
    color: var(--muted);
  }
  table.examples {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 8px;
    font-size: 12.8px;
  }
  table.examples th, table.examples td {
    border: 1px solid var(--line);
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
  }
  table.examples th {
    background: var(--bg-soft);
    font-weight: 700;
    width: 90px;
  }
  .pattern {
    font-size: 12.8px;
    color: var(--muted);
    margin: 6px 0 0;
  }
  .pattern b { color: var(--navy); }

  /* 콜아웃 */
  .callout {
    border-left: 4px solid var(--alert);
    background: var(--alert-bg);
    padding: 12px 16px;
    margin: 10px 0 4px;
    font-size: 12.8px;
  }
  .callout .lead {
    font-weight: 700;
    color: var(--alert);
    margin: 0 0 4px;
  }
  .callout p { margin: 4px 0; }

  footer.note {
    margin-top: 28px;
    font-size: 11.8px;
    color: var(--muted);
    border-top: 1px solid var(--line);
    padding-top: 12px;
  }
  footer.note ul { margin: 4px 0; padding-left: 18px; }
</style>
</head>
<body>
<div class="wrap">

  <header class="title-block">
    <h1>CS 문의 집계 리포트</h1>
    <div class="meta">집계 기간: 2026-08-24 ~ 2026-08-30 (7일) · 채널: 이메일·채팅·게시판 혼합 · 총 27건 (잡음 2건 제외)</div>
  </header>

  <div class="chip-row">
    <span class="chip total">총 문의 <b>27건</b></span>
    <span class="chip">배송 지연 <b>12건</b></span>
    <span class="chip">결제·환불 오류 <b>5건</b></span>
    <span class="chip">상품 정보 문의 <b>4건</b></span>
    <span class="chip">로그인·계정 문제 <b>3건</b></span>
    <span class="chip">기타 <b>3건</b></span>
  </div>

  <!-- 비중이 큰 유형: 콜아웃 포함 -->
  <section class="type-section">
    <div class="type-head">
      <h2>1. 배송 지연</h2>
      <span class="count">12건 (전체의 44%)</span>
    </div>
    <table class="examples">
      <tr><th>예시 1</th><td>"주문한 지 5일째인데 계속 배송 준비 중이라고만 뜬다. 언제 오는지 알고 싶다."</td></tr>
      <tr><th>예시 2</th><td>"택배사 조회를 눌러도 정보가 안 뜬다. 분실된 게 아닌지 걱정된다."</td></tr>
      <tr><th>예시 3</th><td>"주말 지나면 온다고 안내받았는데 다음 주말이 돼도 안 왔다."</td></tr>
    </table>
    <p class="pattern"><b>공통 패턴</b> 주문 후 3일 이상 경과한 시점에 몰려 접수됨. 특정 택배사 경유 건에 집중되는 경향이 있는 것으로 보임.</p>
    <div class="callout">
      <p class="lead">전체 문의의 44%를 차지하는 최다 유형</p>
      <p>비중이 특히 크므로 개별 응대만으로는 재발이 반복될 가능성이 있음. 배송 파트너사 처리 프로세스나 배송 예정일 안내 문구 자체를 점검할 필요가 있는 것으로 보임.</p>
    </div>
  </section>

  <section class="type-section">
    <div class="type-head">
      <h2>2. 결제·환불 오류</h2>
      <span class="count">5건 (전체의 19%)</span>
    </div>
    <table class="examples">
      <tr><th>예시 1</th><td>"결제는 됐다고 문자가 왔는데 주문 내역에는 안 뜬다."</td></tr>
      <tr><th>예시 2</th><td>"환불 신청한 지 일주일이 지났는데 아직 입금이 안 됐다."</td></tr>
    </table>
    <p class="pattern"><b>공통 패턴</b> 결제 완료 알림과 주문 내역 반영 사이에 시차가 있는 건, 환불 처리 지연 건 두 갈래로 나뉨.</p>
  </section>

  <section class="type-section">
    <div class="type-head">
      <h2>3. 상품 정보 문의</h2>
      <span class="count">4건 (전체의 15%)</span>
    </div>
    <table class="examples">
      <tr><th>예시 1</th><td>"사이즈 표에 나온 수치가 실측이랑 맞는 건지 궁금하다."</td></tr>
      <tr><th>예시 2</th><td>"색상이 사진이랑 실제로 같은지 문의드린다."</td></tr>
    </table>
    <p class="pattern"><b>공통 패턴</b> 구매 전 문의가 대부분이며 상품 상세 페이지 정보로는 확신이 서지 않아 재차 묻는 경우로 보임.</p>
  </section>

  <section class="type-section">
    <div class="type-head">
      <h2>4. 로그인·계정 문제</h2>
      <span class="count">3건 (전체의 11%)</span>
    </div>
    <table class="examples">
      <tr><th>예시 1</th><td>"비밀번호 재설정 메일이 안 온다."</td></tr>
      <tr><th>예시 2</th><td>"소셜 로그인 연동이 풀려서 다시 가입해야 하는지 물어본다."</td></tr>
    </table>
    <p class="pattern"><b>공통 패턴</b> 메일 미수신, 소셜 로그인 연동 해제 두 유형이 섞여 있어 원인이 서로 다른 것으로 보임.</p>
  </section>

  <section class="type-section">
    <div class="type-head">
      <h2>5. 기타</h2>
      <span class="count">3건 (전체의 11%)</span>
    </div>
    <table class="examples">
      <tr><th>예시 1</th><td>"이벤트 쿠폰이 적용되는 상품 범위를 알고 싶다."</td></tr>
      <tr><th>예시 2</th><td>"오프라인 매장에서도 교환이 되는지 물어본다."</td></tr>
    </table>
    <p class="pattern"><b>공통 패턴</b> 단발성 문의로 서로 다른 주제라 별도 유형으로 묶기 어려워 기타로 분류함.</p>
  </section>

  <footer class="note">
    <p>제외 건수: 2건(광고성 회신, 시스템 자동 발신 메일로 문의로 보기 어려워 집계에서 제외함)</p>
    <p>분류 기준: 문의 원문에서 파악되는 핵심 요구사항 1개를 기준으로 유형을 부여함. 여러 이슈가 섞인 문의는 더 핵심적인 요구사항 쪽으로 분류함.</p>
    <ul>
      <li>원인·시사점 서술 중 "~로 보임" 표현은 데이터만으로 확정할 수 없는 추정임을 뜻함.</li>
      <li>유형별 건수 합계와 상단 chip 표기가 일치함을 확인함(27건 = 12+5+4+3+3).</li>
    </ul>
  </footer>

</div>
</body>
</html>
```

## 마무리 검증 체크리스트

- [ ] 유형별 건수 합 == 총 문의 건수(제외 건수는 별도 표기)
- [ ] 상단 chip 건수 == 본문 섹션 건수
- [ ] 콜아웃은 실제 비중 기준(대략 20% 이상 또는 최다 1~2개)을 충족하는 유형에만 붙였는지
- [ ] 대표 예시가 원문 왜곡 없이 요약되었는지
- [ ] 추정 서술에 "~로 보임" 등 추정 표현이 붙어 있는지 (단정형 문장 없음)
- [ ] em대시(-) 0개
- [ ] 동일 파일명 기존 산출물 덮어쓰기 여부 확인
