---
name: meeting-transcript-organizer
description: 통화 녹취록이나 미팅 메모처럼 길고 비정형인 원본을 다시 듣거나 처음부터 읽지 않고도 파악할 수 있도록, 격식 있는 회의록이 아니라 "주제별 리스트"로 가볍고 빠르게 정리한다. "녹취록 정리해줘", "통화 내용 정리해줘", "미팅 메모 주제별로 뽑아줘", "통화녹취 정리해줘", "회의 녹음 텍스트 정리", "미팅 노트 주제별로 나눠줘" 요청 시 사용한다.
---

# meeting-transcript-organizer

## 이 스킬은 무엇을 하는가

통화 녹취록, 화자 구분이 없는 통화 메모, 미팅 중 받아 적은 비정형 텍스트 등 원본이 길고 흐름이 뒤섞여 있어서 사람이 처음부터 다시 읽거나 녹음을 다시 듣기 부담스러운 자료를 입력받는다. 그 원본을 순서 그대로 요약하는 것이 아니라, **논의된 주제 단위로 재구성해서 리스트업**한 HTML 문서로 만든다. 목적은 정확한 격식이 아니라 "몇 분이면 무슨 얘기가 오갔는지 파악되는" 속도와 가독성이다.

## 정식 회의록과의 차이 (중요 - 반드시 먼저 확인)

이 스킬은 **정식 업무회의록을 만들지 않는다.** 참석자·일시·장소·안건 번호·결정사항이 격식을 갖춰 기재되는 공식 문서, 발주처·자문위원회처럼 외부에 보고하거나 대외 증빙으로 남겨야 하는 회의록이 필요하면 `meeting-minutes-writer` 에이전트를 안내하고 이 스킬로 진행하지 않는다.

구분 기준:
- 대외 보고용·증빙용·정식 서명이 필요한 문서 → 이 스킬 아님 (meeting-minutes-writer)
- 본인이나 팀이 빠르게 훑어보기 위한 내부용 정리, "일단 무슨 얘기 나왔는지만 알고 싶다" → 이 스킬

모호하면 사용자에게 "정식 회의록이 필요한지, 빠르게 훑어볼 주제별 정리면 되는지" 먼저 확인한다.

## 입력

- 통화 녹취록 (화자 구분 표기가 있을 수도, 없을 수도 있다 - 예: "A:", "김부장:", "고객:" 형태이거나 아무 표시 없이 통째로 이어진 텍스트일 수 있다)
- 미팅 중 받아 적은 비정형 메모
- 위 두 종류가 여러 개(여러 통화, 여러 미팅) 함께 주어질 수도 있다

## 처리 절차

### 1단계 - 원본 형식 파악

먼저 원본을 훑어 화자 표기가 있는지 확인한다. "이름:", "화자1:", "고객:"처럼 명시적 태그가 있으면 그대로 신뢰한다. 태그가 없고 문맥만으로 화자를 구분해야 하는 경우, 확신이 설 때만 화자를 표기하고 확신이 없으면 임의로 이름을 단정하지 않는다(아래 3단계 참고).

여러 원본이 함께 주어지면 각 원본을 구분할 수 있는 표시(파일명, 통화 일시 등)를 섹션이나 항목 옆에 남긴다.

### 2단계 - 주제 단위로 재구성

원본을 처음부터 끝까지 통독하며 다뤄진 주제를 뽑는다. 같은 주제가 대화 중 여러 번 왔다 갔다 하는 경우가 많으므로, **원문 등장 순서가 아니라 주제 기준으로 흩어진 내용을 한 섹션에 모은다.** 주제 개수는 원본 분량에 맞게 자연스럽게 정한다 - 개수를 억지로 맞추지 않는다.

각 섹션은 다음으로 구성한다:
- 섹션 제목: 논의 주제를 한 줄로
- 불릿 리스트: 그 주제에서 나온 핵심 내용만 (잡담, 인사말, 본론과 무관한 여담은 제외)

### 3단계 - 화자 처리 규칙

- 원본에 화자가 명시된 경우: 발언 앞에 화자명을 그대로 표기한다.
- 원본에 화자 표기가 없지만 문맥상(예: 질문하는 쪽과 답하는 쪽이 뚜렷이 구분되는 경우) 화자를 구분할 근거가 충분한 경우에만 표기하되, 이름을 지어내지 말고 "고객", "담당자" 같은 원본 근거가 있는 역할명만 쓴다.
- 화자 구분이 불확실하면 절대로 임의로 단정하지 않는다. 이때는 **"발언자 불명"** 또는 **"확인 필요"**로 표기한다.
- 원본 자체에 화자 개념이 없는 통메모라면 화자 표기 없이 요약체(개조식)로만 정리한다.

### 4단계 - 사실과 추정을 문장에서 구분

- 원본에 명시적으로 나온 내용은 단정형 문장으로 그대로 정리한다.
- 원본에 직접 나오지 않았지만 문맥상 정리자가 유추한 내용(예: 애매한 표현을 정리자가 해석해서 요약한 경우)은 반드시 **"~로 보임", "~로 추정됨", "(추정)"** 같은 표현을 붙여 사실과 구분한다.
- 확신이 없는 내용을 사실인 것처럼 단정문으로 적지 않는다. 애매하면 추정 표현을 쓰거나 "확인 필요"로 남긴다.

### 5단계 - 액션아이템 추출

대화 중 후속 조치로 언급된 내용(예: "~하기로 함", "확인해서 전달하겠다", "다음 주까지 보내주기로")을 모아 **마지막 별도 섹션**으로 분리한다.
- 담당자나 기한이 원본에 언급됐으면 함께 기록한다.
- 언급되지 않았으면 빈칸으로 두고 지어내지 않는다.

### 6단계 - HTML로 조립

아래 "HTML 템플릿" 섹션의 구조와 CSS를 그대로 사용해서 실제 정리 내용으로 채운다. 섹션 개수, 불릿 개수, 액션아이템 개수는 원본 분량에 맞게 자유롭게 늘리거나 줄인다 - 템플릿의 예시 항목 수를 그대로 맞출 필요는 없다.

### 7단계 - 저장

결과 HTML은 원본 파일명을 활용해 `{원본파일명}-정리.html` 형태로 저장하는 것을 기본으로 하되, 사용자가 저장 위치나 파일명을 지정하면 그것을 따른다. 기존 동명 파일이 있으면 임의로 덮어쓰지 않고 사용자에게 확인한다.

## 자주 하는 실수 (체크)

- 원문 순서 그대로 나열하고 "주제별 정리"라고 부르는 것 - 반드시 흩어진 발언을 주제로 재취합할 것
- 화자를 확신 없이 이름으로 단정하는 것 - "발언자 불명"으로 남길 것
- 정리자의 해석을 사실처럼 단정문으로 쓰는 것 - 추정 표현 누락 주의
- 액션아이템에 없는 담당자·기한을 채워 넣는 것 - 없으면 비워둘 것
- 정식 회의록처럼 참석자/일시/장소를 격식 갖춰 표 형식으로 만드는 것 - 이 스킬은 그런 격식 문서가 아니다 (필요하면 최소한의 메타정보 한두 줄만)
- em-dash(—) 사용 - 하이픈(-)이나 가운뎃점(·)으로 대체

## HTML 템플릿

아래는 예시 통화 녹취록 데이터로 채운 완성 샘플이다. 실제 작업 시 이 구조와 CSS를 그대로 유지하고 내용만 교체한다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>녹취록 정리 - 홈페이지 리뉴얼 통화 (2026-08-20)</title>
<style>
  :root {
    --ink: #1a1a2e;
    --ink-soft: #55566e;
    --line: #1a1a2e;
    --bg: #ffffff;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 40px 20px 80px;
    background: var(--bg);
    color: var(--ink);
    font-family: "Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    line-height: 1.65;
  }
  .container {
    max-width: 820px;
    margin: 0 auto;
  }
  header.doc-header {
    padding-bottom: 20px;
    border-bottom: 2px solid var(--line);
    margin-bottom: 8px;
  }
  header.doc-header h1 {
    font-size: 22px;
    margin: 0 0 10px;
    letter-spacing: -0.3px;
  }
  .doc-meta {
    font-size: 13px;
    color: var(--ink-soft);
  }
  .doc-meta span + span::before {
    content: "·";
    margin: 0 8px;
  }
  section.topic {
    padding: 24px 0;
    border-bottom: 1px solid var(--line);
  }
  section.topic:last-of-type {
    border-bottom: none;
  }
  section.topic h2 {
    font-size: 16px;
    margin: 0 0 12px;
  }
  section.topic ul {
    margin: 0;
    padding-left: 20px;
  }
  section.topic li {
    margin-bottom: 8px;
    font-size: 14px;
  }
  .speaker {
    font-weight: 700;
    margin-right: 4px;
  }
  .speaker.unknown {
    font-weight: 400;
    font-style: italic;
    color: var(--ink-soft);
  }
  .estimate {
    color: var(--ink-soft);
    font-style: italic;
  }
  section.actions {
    padding-top: 24px;
    border-top: 2px solid var(--line);
    margin-top: 8px;
  }
  section.actions h2 {
    font-size: 16px;
    margin: 0 0 14px;
  }
  table.action-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
  }
  table.action-table th,
  table.action-table td {
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1px solid #d8d8e0;
    vertical-align: top;
  }
  table.action-table th {
    font-weight: 700;
    color: var(--ink-soft);
    font-size: 12px;
    border-bottom: 1px solid var(--line);
  }
  .empty-cell {
    color: var(--ink-soft);
  }
  footer.doc-footer {
    margin-top: 40px;
    font-size: 12px;
    color: var(--ink-soft);
  }
  @media (max-width: 600px) {
    body { padding: 24px 14px 60px; }
    header.doc-header h1 { font-size: 19px; }
  }
</style>
</head>
<body>
  <div class="container">
    <header class="doc-header">
      <h1>홈페이지 리뉴얼 통화 정리</h1>
      <div class="doc-meta">
        <span>원본: 2026-08-20_고객사통화녹취.txt</span>
        <span>정리일: 2026-08-31</span>
        <span>형식: 주제별 리스트 (정식 회의록 아님)</span>
      </div>
    </header>

    <section class="topic">
      <h2>일정</h2>
      <ul>
        <li><span class="speaker">고객</span>오픈 목표일은 다음 달 말로 희망한다고 밝힘.</li>
        <li><span class="speaker">담당자</span>현재 진행 속도면 목표일 안에 1차 디자인 시안까지는 가능하다고 답변.</li>
        <li><span class="speaker unknown">발언자 불명</span>중간 검수 일정을 격주로 하자는 제안이 나왔으나 누가 먼저 제안했는지는 <span class="estimate">확인 필요</span>.</li>
      </ul>
    </section>

    <section class="topic">
      <h2>예산</h2>
      <ul>
        <li><span class="speaker">고객</span>기존 견적서 대비 추가 페이지 3개를 넣고 싶다고 요청.</li>
        <li><span class="speaker">담당자</span>추가 페이지는 별도 견적으로 산정해서 다시 안내하겠다고 답변.</li>
        <li>결제 방식은 <span class="estimate">계약금 후 잔금 분할로 가는 것으로 보임</span> - 통화에서 금액·비율이 명확히 확정되지는 않음.</li>
      </ul>
    </section>

    <section class="topic">
      <h2>디자인 방향</h2>
      <ul>
        <li><span class="speaker">고객</span>기존 사이트보다 밝은 톤을 원한다고 언급.</li>
        <li><span class="speaker">고객</span>경쟁사 사이트 A, B를 예시로 제시하며 참고해달라고 요청.</li>
        <li><span class="speaker">담당자</span>참고 사이트 반영한 시안 2개를 준비해 다음 미팅 때 보여주겠다고 답변.</li>
      </ul>
    </section>

    <section class="topic">
      <h2>기타 논의</h2>
      <ul>
        <li><span class="speaker unknown">확인 필요</span>모바일 앱 연동 여부가 잠깐 언급됐으나 이번 프로젝트 범위인지는 통화상 명확히 정리되지 않음.</li>
      </ul>
    </section>

    <section class="actions">
      <h2>액션아이템</h2>
      <table class="action-table">
        <thead>
          <tr>
            <th>내용</th>
            <th>담당자</th>
            <th>기한</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>추가 페이지 3개에 대한 별도 견적서 작성</td>
            <td>담당자</td>
            <td><span class="empty-cell">언급 없음</span></td>
          </tr>
          <tr>
            <td>참고 사이트(A, B) 반영한 디자인 시안 2개 준비</td>
            <td>담당자</td>
            <td>다음 미팅 전</td>
          </tr>
          <tr>
            <td>모바일 앱 연동이 이번 범위에 포함되는지 재확인</td>
            <td><span class="empty-cell">언급 없음</span></td>
            <td><span class="empty-cell">언급 없음</span></td>
          </tr>
        </tbody>
      </table>
    </section>

    <footer class="doc-footer">
      이 문서는 통화 녹취록을 주제별로 재구성한 내부 참고용 정리이며, 정식 회의록을 대체하지 않습니다.
    </footer>
  </div>
</body>
</html>
```

### 템플릿 적용 시 유의사항

- `.estimate`, `.speaker.unknown` 클래스는 반드시 실제로 원본에 없는 추정·불확실 내용에만 붙인다. 확정된 사실에 습관적으로 붙이지 않는다.
- 액션아이템 표에서 담당자·기한이 원본에 없으면 `empty-cell` 클래스로 "언급 없음"을 표기하고 빈칸을 지어내지 않는다.
- 섹션(`section.topic`) 개수와 각 섹션의 불릿 개수는 원본 분량에 맞춰 자유롭게 조정한다.
- 카드형 배경색, 그라데이션, 원형·파스텔 배지, 중첩 box-shadow는 쓰지 않는다. 구분은 항상 라인(`border-top`/`border-bottom`)으로만 한다.
- 포인트 색상을 넣지 않는다. 네이비(`--ink`)와 그 옅은 톤(`--ink-soft`)만 사용한다.
