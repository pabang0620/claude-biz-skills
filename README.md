# Claude Biz Skills

1인사업자·소상공인을 위한 Claude Code 스킬 모음

## 설치 및 사용법

이 레포는 Claude Code의 스킬(`SKILL.md`) 9개를 모아둔 것이다. 사용 방법은 두 가지다.

**필요한 스킬만 골라 복사** (권장)

원하는 스킬 폴더를 자기 프로젝트의 `.claude/skills/` 아래로 그대로 복사하면 된다.

```bash
cp -r skills/service-contract-writer ~/your-project/.claude/skills/
```

여러 개를 한 번에 넣고 싶으면 폴더를 여러 개 반복해서 복사하면 된다.

**레포 전체를 클론해서 통째로 사용**

```bash
git clone https://github.com/<owner>/claude-biz-skills.git
```

클론한 `skills/` 디렉토리를 프로젝트의 `.claude/skills/`로 지정하거나, 필요할 때마다 위 방식대로 개별 복사해서 쓰면 된다.

복사 후에는 Claude Code 세션에서 SKILL.md의 `description`에 적힌 트리거 문구(아래 표 참고)를 말하면 해당 스킬이 자동으로 활성화된다.

## 스킬 목록

| 이름 | 설명 | 트리거 예시 | 상태 |
|---|---|---|---|
| [service-contract-writer](skills/service-contract-writer/SKILL.md) | 프리랜서/외주 용역계약서를 표준 조항(제1조~제9조+서명란) 양식 그대로 인쇄 최적화 HTML로 작성 | "계약서 써줘", "용역계약서 만들어줘" | 완료 |
| [quote-comparison](skills/quote-comparison/SKILL.md) | 여러 업체 견적서를 가격·조건·납기 기준으로 비교표 생성 (최저가·유리조건 강조) | "견적 비교해줘", "업체별 견적서 비교표 만들어줘" | 완료 |
| [cs-inquiry-triage](skills/cs-inquiry-triage/SKILL.md) | 고객 문의 뭉치를 이슈 유형별로 자동 집계·정리 | "고객문의 정리해줘", "CS 티켓 집계해줘" | 완료 |
| [resume-screener](skills/resume-screener/SKILL.md) | 지원자 이력서 다건을 채용조건 기준 비교표로 정리, 특이사항 열 포함 (합격판정 없음) | "지원자 이력서 비교해줘", "채용 스크리닝 해줘" | 완료 |
| [meeting-transcript-organizer](skills/meeting-transcript-organizer/SKILL.md) | 녹취록/통화메모를 주제별 리스트 + 인원별 할일 섹션으로 정리 | "녹취록 정리해줘", "통화 내용 정리해줘" | 완료 |
| [chat-log-summarizer](skills/chat-log-summarizer/SKILL.md) | 긴 업무 대화 로그를 주제별 대화 정리 + 결정사항·남은 이슈·담당자별 할일로 재구성 | "카톡방 정리해줘", "슬랙 대화 정리해줘" | 완료 |
| [agent-evaluator](skills/agent-evaluator/SKILL.md) | Claude Code 에이전트 정의파일(.md) 품질을 등급별로 정적 평가 (점수는 매기지 않음) | "에이전트 평가해줘", "이 에이전트 정의파일 점검해줘" | 완료 |
| [sales-data-analyzer](skills/sales-data-analyzer/SKILL.md) | 판매 주문 CSV를 KPI·기간비교(막대그래프)·RFM 고객 세그먼트 리포트로 변환 | "매출 CSV 분석해줘", "재구매율 분석" | 완료 |
| [invoice-organizer](skills/invoice-organizer/SKILL.md) | 흩어진 청구서·영수증을 정리된 매입 기록 표로 변환 | "청구서 정리해줘", "영수증 뭉치 정리해줘" | 완료 |

## License

MIT
