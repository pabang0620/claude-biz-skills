---
name: agent-evaluator
description: Claude Code 서브에이전트 정의파일(.claude/agents/*.md)의 품질을 정적 분석으로 평가한다. frontmatter(name/description/tools/model) 구성, description의 트리거 키워드 명확성, tools 최소권한 여부, 본문 길이·구조, 역할 모호성·경계 누락을 점검해 CRITICAL/HIGH/MEDIUM/LOW 등급의 발견사항과 HTML 리포트를 만든다. "에이전트 평가해줘", "이 에이전트 정의파일 점검해줘", "서브에이전트 품질 확인", "이 .md 배포해도 되는지 봐줘" 같은 요청에 사용한다. 점수(예: 87/100)는 매기지 않는다 - 등급별 발견사항과 근거 인용이 산출물의 전부다.
---

# agent-evaluator

Claude Code 서브에이전트 정의파일(`.claude/agents/*.md`) 1개를 읽고, 배포 전에 흔히 놓치는 구조적 결함을 정적으로 찾아 등급을 매긴 HTML 리포트를 만드는 스킬이다. 에이전트를 실제로 실행시켜 행동을 관찰하지 않는다 - 정의파일 텍스트만 읽고 판단하는 정적 분석 전용이다.

## 이 스킬이 하지 않는 것

- **점수를 매기지 않는다.** 87/100, 92점, 퍼센트, 별점, 게이지 같은 수치화된 품질 지표를 만들지 않는다. 산출물은 등급(CRITICAL/HIGH/MEDIUM/LOW)이 붙은 발견사항 목록과 그 근거뿐이다.
- **"N점 이상 될 때까지 반복 개선" 같은 재평가 루프를 만들지 않는다.** 한 번 훑고 발견사항을 보고하면 그 라운드는 끝이다. 사용자가 정의파일을 고친 뒤 다시 봐달라고 명시적으로 요청하면 그때 새로 평가하되, Claude가 먼저 "다시 평가해볼까요"를 반복 제안하지 않는다.
- **정의파일을 직접 고치지 않는다.** 발견사항마다 개선 제안을 1줄씩 달아줄 뿐, 실제 수정은 사용자나 별도 구현 작업의 몫이다.
- **에이전트를 스폰해 실행 검증(동적 테스트)하지 않는다.** 이 스킬은 텍스트 정적 분석에 한정된다. 실제로 프롬프트를 던져 행동을 관찰하는 동적 검증까지 필요하면 이 스킬의 범위를 벗어난다는 점을 사용자에게 알린다.

## 평가 원칙

1. **근거 없는 발견사항은 리포트에 올리지 않는다.** 모든 발견사항은 정의파일의 실제 텍스트(라인 번호 또는 필드명 + 원문 발췌)를 근거로 인용해야 한다. "아마도", "~일 것 같다" 같은 추측성 판정은 하지 않는다 - 근거를 댈 수 없으면 그 발견사항은 버린다.
2. **문제 없는 항목도 침묵하지 않는다.** 5개 평가 항목 중 결함이 없는 항목은 "문제 없음"으로 명시적으로 적는다. 침묵은 "확인 안 함"과 "문제 없음"을 구분하지 못하게 만든다.
3. **등급은 심각도 기준이지 개수 기준이 아니다.** 같은 종류의 결함이 여러 군데 있어도 등급을 부풀리지 않는다 (예: 트리거 키워드 부재는 몇 번이 반복돼도 HIGH이지 CRITICAL이 되지 않는다).
4. **상단에 종합 판정 한 줄을 반드시 둔다.** 리포트를 처음 여는 사람이 스크롤 없이 "배포해도 되는가"를 알 수 있어야 한다.

## 등급 기준

| 등급 | 의미 | 전형적 사례 |
|---|---|---|
| CRITICAL | 배포하면 실제로 오작동하거나 사고를 낼 수 있는 결함 | `model` 필드 누락/오기, 본문에 "수정하지 않는다"고 써놓고 `tools`에 `Write`/`Edit`가 있음, 파괴적 명령(`rm`, `git push --force` 등) 사용 범위를 제한하는 서술이 전혀 없는데 `Bash`를 무제한 보유 |
| HIGH | 자동 위임이 실패하거나 다른 에이전트와 역할이 충돌하는 결함 | `description`에 "언제 쓰는지"가 없어 라우팅이 안 됨, 다른 에이전트와 담당 영역이 완전히 겹치는데 경계 설명이 없음, `tools`가 아예 명시되지 않아 전체 상속됨 |
| MEDIUM | 품질은 떨어지지만 당장 오작동으로 이어지지는 않는 것 | 본문이 500줄에 근접/초과, 판단 규칙과 긴 코드 예제가 뒤섞여 있음, 읽기 전용 역할인데 굳이 필요 없어 보이는 도구가 하나 끼어 있음 |
| LOW | 개선하면 좋지만 급하지 않은 것 | 예외 상황(입력 모호, 다중 매치, 대상 없음) 처리가 한 줄도 없음, 경계 설명이 있긴 하지만 인접 에이전트 이름을 안 밝힘 |

## 평가 절차

### Step 0. 평가 대상 확정

- 사용자가 절대경로를 줬으면 그 파일을 Read한다. 파일이 없으면 "대상 파일 없음: {경로}"를 보고하고 중단한다.
- 이름만 줬으면 `.claude/agents/` 아래에서 `{이름}*.md`로 Glob한다. 프로젝트 스코프(`<repo>/.claude/agents/`)와 사용자 홈 스코프(`~/.claude/agents/`)가 둘 다 있으면 둘 다 뒤진다.
  - 매치 0개 - "평가 대상을 찾을 수 없습니다. 절대 경로를 알려주세요."라고 안내하고 중단한다.
  - 매치 2개 이상이고 내용이 다르면 - 임의로 하나를 고르지 않는다. 후보 경로·최종수정일을 나열하고 어느 것을 평가할지 사용자에게 확인한다.
  - 매치 2개 이상이고 내용이 바이트 단위로 같으면 - MEDIUM 발견사항으로 "동기화 사본 존재(경로 나열)"를 리포트에 남기고, 최신 수정 파일 하나로 평가를 계속한다.
- frontmatter(`---`로 감싼 블록)를 파싱한다. YAML이 깨져 있으면 파싱 가능한 필드만으로 진행하고 리포트 상단에 "frontmatter 파싱 이슈" 경고를 남긴다.

### Step 1. Frontmatter 검사

- **name**: 소문자와 하이픈만 쓰였는지(`^[a-z][a-z0-9-]*$`) 확인한다. 파일명과 `name` 값이 다르면 LOW로 지적한다. 같은 `.claude/agents/` 디렉토리에서 `Grep(pattern="^name: {값}$")`로 중복 여부를 확인하고, 중복이면 Step 0의 판정을 그대로 승계한다.
- **description**: 존재 여부, 그리고 "무엇을 하는가"와 "언제 쓰는가(트리거 조건)"가 둘 다 담겼는지 확인한다. 트리거 서술이 아예 없으면 HIGH. Step 2에서 더 정밀하게 다시 본다.
- **tools**: 배열로 명시돼 있는지 확인한다. 필드 자체가 없으면(전체 도구 상속) HIGH로 지적한다 - 의도치 않은 과잉 권한을 못 걸러낸다. 개별 도구의 적절성은 Step 3에서 다룬다.
- **model**: 필드가 있는지 확인한다. 없으면 CRITICAL(어떤 모델로 실행될지 정의파일만 보고 알 수 없음). 있으면 프로젝트에 모델 정책이 문서화돼 있는 경우(예: 로컬 CLAUDE.md의 "sonnet 고정" 같은 규칙) 그 값과 일치하는지 대조하고, 불일치하면 근거 규칙을 인용해 지적한다. 프로젝트에 그런 정책 문서가 없으면 필드 존재 여부만 확인하고 값 자체는 판단하지 않는다.
- 스킬 전용 필드(`allowed-tools`, `context`, `disable-model-invocation` 등)가 에이전트 frontmatter에 섞여 있으면 CRITICAL("frontmatter 오염 - 스킬 필드가 에이전트에 혼입")로 지적한다.

### Step 2. 트리거 명확성

`description` **텍스트만** 놓고 판단한다 - 본문을 참고하지 않는다. 실제 자동 위임은 이 한 줄만 보고 결정되기 때문이다.

- 이 설명만 읽고 "어떤 사용자 요청이 오면 이 에이전트가 뽑히는가"를 구체적으로 짚을 수 있는가? 짚을 수 없으면 HIGH.
- "~시 사전에 적극 활용", "use proactively when", "use when" 같은 명시적 트리거 문구, 또는 실제 사용자가 쓸 법한 한국어/영어 표현 예시가 있는가? 없으면 HIGH.
- 인접한 다른 에이전트(같은 디렉토리의 다른 `.md` 파일)와 도메인 키워드가 겹치는데 "이런 요청은 저 에이전트로 간다"는 경계 서술이 없는가? 있으면 MEDIUM(Step 5와 연결).
- description이 지나치게 짧아(한 문장, 트리거 단서 없음) 판단 근거 자체가 부족하면 그 사실 자체를 HIGH로 남긴다.

### Step 3. 도구 최소권한

- 본문에 "수정하지 않는다", "발견·보고만", "읽기 전용", "진단 전용" 같은 역할 제한 서술이 있는데 `tools`에 `Write`나 `Edit`가 있으면 CRITICAL(자기모순 - 실제로는 수정할 수 있는 도구를 쥐고 있음).
- 조사·리서치·감사류 역할인데 `Bash`가 무제한으로 있고, 어떤 명령이 허용/금지인지 본문에 범위 서술이 전혀 없으면 MEDIUM 이상(파괴적 명령 실행 여지 - 역할이 실제로 시스템을 바꾸는 쪽이면 CRITICAL까지 격상).
- 본문에서 다른 에이전트를 스폰하는 절차(예: "~에게 위임한다", "병렬로 실행한다")가 서술돼 있는데 `tools`에 `Agent`가 없으면 HIGH(실행 불가능한 절차가 문서화됨). 반대로 `Agent`가 있는데 본문 어디에도 스폰 절차가 없으면 LOW(불필요한 권한 소지 가능성, 확신이 없으면 LOW로 낮춰 보고).
- 파일 생성/수정이 필요 없는 순수 조회형 역할(리뷰어, 검증기, 감사기)인데 `Write`/`Edit`가 있으면 MEDIUM 이상으로 지적한다.

### Step 4. 본문 길이/구조

- `wc -l`로 본문 줄 수를 센다. 500줄을 넘으면 CRITICAL, 400~500줄이면 MEDIUM으로 "분할 검토" 권고를 남긴다.
- 긴 코드 블록(펜스 ```로 감싼 구간)이 본문 여러 곳에 흩어져 판단 규칙과 뒤섞여 있으면 MEDIUM으로 "구현 예제를 참조 파일로 분리 권장"을 남긴다. 코드 예제 자체가 나쁜 것이 아니라, 판단 기준(언제·왜)과 구현 골격(어떻게)이 분리 안 된 게 문제라는 점을 근거에 명시한다.
- 섹션 헤더(`##`, `###`)가 전혀 없이 긴 산문으로만 이어져 있으면 LOW로 "구조화 부족"을 남긴다.

### Step 5. 모호성/누락

- "역할 범위", "경계", "이 에이전트가 하지 않는 것" 같은 섹션이 있는지 확인한다. 없고 동시에 Step 2에서 인접 에이전트와의 키워드 중복이 확인됐다면 HIGH로 격상한다(경계 없음 + 실제 중복 위험이 겹치는 경우).
- 예외 상황 처리 서술이 있는지 본다 - 입력이 모호할 때, 대상 파일이 여러 개일 때, 필요한 정보가 없을 때 무엇을 하는지. 전혀 없으면 LOW(성격상 필요 없는 단순 역할이면 스킵해도 됨 - 판단해서 적용).
- 같은 문제(예: "코드 수정 여부")에 대해 본문 안에서 서로 다른 문장이 상충하는 서술을 하고 있으면 CRITICAL로 지적한다(자기모순은 실행 시점에 어느 쪽을 따를지 알 수 없다).

### Step 6. 종합 판정과 리포트 작성

- CRITICAL이 1건이라도 있으면 종합 판정은 "CRITICAL 항목 수정 후 배포 권장".
- CRITICAL은 없고 HIGH가 있으면 "HIGH 항목 검토 후 배포 권장".
- CRITICAL·HIGH가 없고 MEDIUM/LOW만 있으면 "배포 가능 (경미한 개선사항 있음)".
- 아무 발견사항도 없으면 "배포 가능".
- 아래 템플릿을 기반으로 실제 발견사항을 채운 HTML을 만들고, 평가 대상 파일과 같은 디렉토리(또는 사용자가 지정한 경로)에 `<에이전트이름>-eval-report.html`로 저장한다. 저장 후 절대경로를 사용자에게 안내한다. Claude Code 환경에 Artifact 발행 도구가 있고 사용자가 화면에서 바로 보길 원하면 그걸로 발행해도 되지만, 기본 산출물은 로컬 HTML 파일이다.

## HTML 리포트 템플릿

아래는 실제로 채워 넣은 완성 샘플이다. 진짜 평가에서는 `{{ }}` 표시가 없는 것에서 보듯 발견사항 전체를 대상 파일의 실측 내용으로 교체해서 쓴다 - 이 샘플의 발견사항(예시로 든 `csv-importer` 에이전트)은 템플릿 구조를 보여주기 위한 것이지 실제 평가 결과가 아니다.

```html
<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>에이전트 정의파일 평가 - csv-importer</title>
<style>
  :root {
    --navy: #1a1a2e;
    --ink: #1a1a1a;
    --line: #e0e0e0;
    --critical: #a4322c;
    --critical-bg: #fbf2f1;
    --high: #8a5a1e;
    --high-bg: #faf5ec;
    --gray: #666666;
    --gray-bg: #f5f5f5;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: #f5f5f7;
    color: var(--ink);
    font-family: "Malgun Gothic","맑은 고딕","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
    line-height: 1.55;
  }
  header {
    background: var(--navy);
    color: #ffffff;
    padding: 24px 32px;
  }
  header h1 { margin: 0 0 6px; font-size: 19px; }
  header .meta { font-size: 13px; color: #c9c9d6; }
  .container { max-width: 920px; margin: 0 auto; padding: 0 20px 60px; }
  .verdict {
    margin-top: 24px;
    padding: 16px 20px;
    background: #ffffff;
    border: 1px solid var(--line);
    border-left: 4px solid var(--navy);
    font-weight: bold;
    font-size: 15px;
  }
  .verdict .sub {
    display: block;
    margin-top: 4px;
    font-weight: normal;
    font-size: 12.5px;
    color: var(--gray);
  }
  .summary-table {
    margin-top: 20px;
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    background: #ffffff;
  }
  .summary-table th, .summary-table td {
    border: 1px solid var(--line);
    padding: 8px 12px;
    text-align: left;
  }
  .summary-table th { background: #ececec; }
  .section { margin-top: 36px; }
  .section h2 {
    font-size: 16px;
    margin: 0 0 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--line);
  }
  .section .count { font-weight: normal; font-size: 13px; color: var(--gray); }
  .finding {
    background: #ffffff;
    border: 1px solid var(--line);
    border-left-width: 4px;
    padding: 14px 16px;
    margin-bottom: 12px;
  }
  .finding.critical { border-left-color: var(--critical); background: var(--critical-bg); }
  .finding.high { border-left-color: var(--high); background: var(--high-bg); }
  .finding.medium { border-left-color: #999999; }
  .finding.low { border-left-color: #bbbbbb; }
  .finding .grade {
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }
  .finding.critical .grade { color: var(--critical); }
  .finding.high .grade { color: var(--high); }
  .finding.medium .grade,
  .finding.low .grade { color: var(--gray); }
  .finding .title { font-size: 14px; font-weight: bold; margin: 4px 0 8px; }
  .finding .quote {
    font-family: "SFMono-Regular", Consolas, monospace;
    font-size: 12.5px;
    background: #f0f0f0;
    border: 1px solid #e2e2e2;
    padding: 8px 10px;
    margin: 8px 0;
    white-space: pre-wrap;
    color: #333333;
  }
  .finding .fix { font-size: 13px; margin-top: 8px; }
  .finding .fix .label { font-weight: bold; }
  .clean-note {
    font-size: 13px;
    color: var(--gray);
    background: var(--gray-bg);
    border: 1px solid var(--line);
    padding: 10px 14px;
  }
  footer {
    margin-top: 40px;
    font-size: 12px;
    color: var(--gray);
    border-top: 1px solid var(--line);
    padding-top: 12px;
  }
</style>
</head>
<body>

<header>
  <h1>에이전트 정의파일 평가 - csv-importer</h1>
  <div class="meta">대상: .claude/agents/csv-importer.md · 평가 방식: 정적 분석 (실행 검증 없음) · 점수 미부여, 등급만 표기</div>
</header>

<div class="container">

  <div class="verdict">
    HIGH 항목 검토 후 배포 권장
    <span class="sub">CRITICAL 0건 · HIGH 2건 · MEDIUM 2건 · LOW 1건</span>
  </div>

  <table class="summary-table">
    <tr><th>평가 항목</th><th>결과</th></tr>
    <tr><td>1. Frontmatter 검사</td><td>문제 없음 (name/description/tools/model 4개 필드 모두 존재)</td></tr>
    <tr><td>2. 트리거 명확성</td><td>HIGH 1건 - description에 "언제 쓰는지" 서술 없음</td></tr>
    <tr><td>3. 도구 최소권한</td><td>HIGH 1건 - 읽기 전용 서술과 tools 권한 불일치</td></tr>
    <tr><td>4. 본문 길이/구조</td><td>MEDIUM 1건 - 코드 예제와 판단 규칙 혼재</td></tr>
    <tr><td>5. 모호성/누락</td><td>MEDIUM 1건, LOW 1건 - 경계 섹션 부재, 예외처리 서술 부족</td></tr>
  </table>

  <div class="section">
    <h2>CRITICAL <span class="count">(0건)</span></h2>
    <div class="clean-note">발견사항 없음.</div>
  </div>

  <div class="section">
    <h2>HIGH <span class="count">(2건)</span></h2>

    <div class="finding high">
      <div class="grade">HIGH</div>
      <div class="title">description에 트리거 조건이 없어 자동 위임이 실패할 수 있음</div>
      <div class="quote">description: "CSV 파일을 읽어 데이터를 정리하는 에이전트."</div>
      <div class="fix"><span class="label">개선 제안:</span> "~요청 시 사전에 적극 활용" 같은 명시적 트리거 문구와, 실제 사용자가 쓸 법한 표현("csv 정리해줘", "이 파일 파싱해줘") 예시를 description에 추가한다.</div>
    </div>

    <div class="finding high">
      <div class="grade">HIGH</div>
      <div class="title">본문은 "원본 파일을 수정하지 않는다"고 서술하지만 tools에 Write/Edit가 포함됨</div>
      <div class="quote">본문 12행: "원본 CSV는 절대 덮어쓰지 않는다"
frontmatter: tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]</div>
      <div class="fix"><span class="label">개선 제안:</span> 새 파일로 산출하는 역할이면 Write는 유지하되 원본 경로에는 쓰지 않는다는 가드를 본문에 명시하거나, 정말 읽기 전용이면 tools에서 Write/Edit를 제거한다.</div>
    </div>
  </div>

  <div class="section">
    <h2>MEDIUM <span class="count">(2건)</span></h2>
    <table class="summary-table">
      <tr><th>항목</th><th>근거</th><th>개선 제안</th></tr>
      <tr>
        <td>본문 구조</td>
        <td>본문 340줄 중 180~260행이 pandas 예제 코드 블록 3개로, 판단 규칙(어떤 구분자를 쓸지 결정하는 기준 등)과 뒤섞여 있음</td>
        <td>구현 예제를 `.claude/agent-refs/csv-importer-examples.md`로 분리하고 본문에는 "언제 이 참조 파일을 읽는지" 표만 남긴다.</td>
      </tr>
      <tr>
        <td>모호성/누락</td>
        <td>"역할 범위" 또는 "경계" 섹션이 본문에 없음. 같은 디렉토리의 spreadsheet-editor와 "표 데이터 정리"라는 키워드가 겹침</td>
        <td>xlsx/스프레드시트 작업은 spreadsheet-editor로 넘긴다는 경계 문장을 description 또는 본문 상단에 추가한다.</td>
      </tr>
    </table>
  </div>

  <div class="section">
    <h2>LOW <span class="count">(1건)</span></h2>
    <table class="summary-table">
      <tr><th>항목</th><th>근거</th><th>개선 제안</th></tr>
      <tr>
        <td>예외 처리</td>
        <td>입력 CSV의 인코딩이 깨졌거나 헤더가 없을 때 어떻게 하는지 본문에 서술 없음</td>
        <td>"헤더 없음/인코딩 불명 시 사용자에게 먼저 확인한다" 같은 한 줄을 추가한다.</td>
      </tr>
    </table>
  </div>

  <footer>
    정적 분석 결과입니다. 실제 프롬프트로 에이전트를 실행해 행동을 관찰하는 동적 검증은 포함하지 않았습니다.
  </footer>

</div>
</body>
</html>
```

## 리포트 작성 시 지켜야 할 것

- CRITICAL·HIGH 발견사항은 개별 카드(`.finding`)로, MEDIUM·LOW는 표로 정리한다 - 표에 담아도 되는 건 "당장 안 터지는" 등급뿐이다.
- CRITICAL·HIGH 카드에만 옅은 경고색 배경과 `border-left: 4px solid`를 쓴다. MEDIUM·LOW는 무채색(회색 계열)만 쓴다.
- 그라데이션, 원형 배지, 파스텔 배지, 중첩 `box-shadow`, 점수/퍼센트 게이지 UI를 넣지 않는다. `border-radius`도 쓰지 않는다(각진 사각형 유지).
- em dash(—)를 쓰지 않는다. 문장 연결에는 하이픈(-)이나 가운뎃점(·)을 쓴다.
- 상단에 종합 판정 한 줄과 등급별 건수 요약을 항상 둔다.
- 발견사항이 0건인 등급 섹션도 지우지 않고 "발견사항 없음"으로 남긴다 - 항목을 평가 안 한 것과 구분하기 위해서다.
