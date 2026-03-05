# GitHub Actions Workflow 아키텍처

이 문서는 자동화된 뉴스 수집 시스템의 전체 구조를 설명합니다.

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Trigger                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ⏰ Schedule (Cron)          🎮 Workflow Dispatch           │
│  매주 월요일 오전 9시(KST)      수동 실행 + 커스터마이징        │
│                                                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Workflow Execution Steps                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. 🔄 Checkout Repository                                   │
│     - 최신 코드 가져오기                                        │
│                                                               │
│  2. 🐍 Setup Python 3.11                                     │
│     - 의존성 캐싱 (빠른 실행)                                   │
│                                                               │
│  3. 📦 Install Dependencies                                  │
│     - pip install -r requirements.txt                        │
│     - google-generativeai, feedparser, etc.                 │
│                                                               │
│  4. 🔍 Check Existing File                                   │
│     - src/content/blog/a11y-news-YYYY-MM-DD.md 확인          │
│                                                               │
│  5. 🚀 Run Python Script                                     │
│     ├─ 입력: GitHub Secrets (GEMINI_API_KEY)                │
│     ├─ 입력: Custom Keywords (optional)                     │
│     ├─ 입력: Custom Prompt (optional)                       │
│     │                                                         │
│     ├─ Google News RSS 검색                                  │
│     ├─ 중복 제거 & 필터링                                      │
│     ├─ Gemini API 호출                                       │
│     └─ 마크다운 파일 생성                                      │
│                                                               │
│  6. ✅ Check Changes                                         │
│     - git status로 변경사항 확인                               │
│                                                               │
│  7. 💾 Commit & Push (변경사항 있을 경우)                      │
│     - git commit with descriptive message                   │
│     - git push to main branch                               │
│                                                               │
│  8. 📊 Generate Summary                                      │
│     - Actions 탭에 실행 결과 표시                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Deployment Pipeline                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. 📝 New Blog Post Committed                               │
│     - src/content/blog/a11y-news-YYYY-MM-DD.md              │
│                                                               │
│  2. 🚀 Deploy Workflow Triggered (deploy.yml)                │
│     - Astro build                                            │
│     - Deploy to GitHub Pages                                 │
│                                                               │
│  3. 🌐 Live Blog Updated                                     │
│     - https://username.github.io/a11y-news            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 실행 흐름

### 정기 실행 (Schedule)

```
일요일 자정(UTC) = 월요일 오전 9시(KST)
         ↓
Workflow 자동 실행
         ↓
기본 키워드로 뉴스 검색
         ↓
Gemini로 요약 및 구조화
         ↓
마크다운 파일 생성
         ↓
자동 커밋 & 푸시
         ↓
Deploy workflow 트리거
         ↓
블로그 업데이트 완료!
```

### 수동 실행 (Workflow Dispatch)

```
GitHub Actions 탭에서 실행
         ↓
커스텀 키워드 입력 (옵션)
"WCAG 3.0, ARIA 1.3"
         ↓
커스텀 프롬프트 입력 (옵션)
"모바일 접근성에 집중해주세요"
         ↓
입력된 키워드로 뉴스 검색
         ↓
커스텀 프롬프트가 Gemini에 전달
         ↓
맞춤형 콘텐츠 생성
         ↓
자동 커밋 & 푸시
         ↓
블로그 업데이트 완료!
```

## 🎯 데이터 흐름

```
┌──────────────────┐
│  Google News RSS │
│                  │
│  • 영문 뉴스     │
│  • 한글 뉴스     │
│  • RSS Feed      │
└────────┬─────────┘
         │
         │ HTTP Request
         ↓
┌──────────────────┐
│ Python Script    │
│ collect_news.py  │
│                  │
│  • 키워드 검색   │
│  • 중복 제거     │
│  • 데이터 정리   │
└────────┬─────────┘
         │
         │ JSON Data
         ↓
┌──────────────────┐
│   Gemini API     │
│  (AI 요약/구조화) │
│                  │
│  • 요약 생성     │
│  • 구조화        │
│  • 출처 명시     │
│  • 결론 작성     │
└────────┬─────────┘
         │
         │ Markdown Text
         ↓
┌──────────────────┐
│  Markdown File   │
│                  │
│  a11y-news-      │
│  YYYY-MM-DD.md   │
└────────┬─────────┘
         │
         │ Git Commit
         ↓
┌──────────────────┐
│ GitHub Repo      │
│  (main branch)   │
└────────┬─────────┘
         │
         │ Deploy Trigger
         ↓
┌──────────────────┐
│  GitHub Pages    │
│  (Live Blog)     │
└──────────────────┘
```

## 🔧 워크플로우 파라미터

### Schedule 트리거

| 파라미터 | 값 | 설명 |
|---------|-----|------|
| `cron` | `0 0 * * 1` | 매주 월요일 오전 9시(KST) |

### Workflow Dispatch 입력

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| `keywords` | string | ❌ | "" | 쉼표로 구분된 검색 키워드 |
| `custom_prompt` | string | ❌ | "" | Gemini에 전달할 추가 지시사항 |

### 환경 변수 (Secrets)

| 이름 | 타입 | 필수 | 설명 |
|-----|------|------|------|
| `GEMINI_API_KEY` | secret | ✅ | Google Gemini API 키 |

## 📊 Workflow 출력

### Git 커밋

```
Add accessibility news for 2026-03-05 (키워드: WCAG 3.0)

Automatically collected and generated by GitHub Actions.

- 수집 일시: 2026-03-05 00:00:00 UTC
- 수집 방식: schedule
- Workflow run: https://github.com/user/repo/actions/runs/12345
```

### GitHub Actions Summary

```
## 🌐 디지털 접근성 뉴스 수집 결과

✅ **상태**: 새 게시물 생성 및 커밋 완료
📄 **파일**: `src/content/blog/a11y-news-2026-03-05.md`

📅 **실행 일시**: 2026-03-05 00:00:00 UTC
🔧 **실행 방식**: schedule
🎯 **커스텀 키워드**: WCAG 3.0, ARIA updates
```

## 🚦 워크플로우 상태

### ✅ 성공 케이스

- 뉴스 수집 성공
- 마크다운 파일 생성
- Git 커밋 및 푸시 완료
- Deploy workflow 자동 트리거

### ⚠️ 부분 성공 케이스

- 뉴스 수집 성공
- 파일 생성 성공
- 하지만 오늘 날짜 파일이 이미 존재
- 변경사항 없음 (커밋 건너뜀)

### ❌ 실패 케이스

- GEMINI_API_KEY 미설정
- API 할당량 초과
- 네트워크 오류
- 뉴스 수집 실패

## 🔐 보안 모델

```
┌─────────────────┐
│ GitHub Secrets  │
│ (Encrypted)     │
│                 │
│ GEMINI_API_KEY  │
└────────┬────────┘
         │
         │ Secure injection
         ↓
┌─────────────────┐
│ Workflow Runner │
│ (Isolated VM)   │
│                 │
│ env:            │
│   GEMINI_API_KEY│
└────────┬────────┘
         │
         │ Environment variable
         ↓
┌─────────────────┐
│ Python Script   │
│                 │
│ os.getenv()     │
└─────────────────┘
```

- ✅ API 키는 암호화되어 저장
- ✅ 로그에 노출되지 않음
- ✅ Public fork에서 접근 불가
- ✅ Workflow 실행 시에만 복호화

## 🎛️ 커스터마이징 예시

### 예시 1: 특정 기술 키워드

**수동 실행 입력:**
```
키워드: React accessibility, Vue a11y, Angular ARIA
추가 지시사항: 프레임워크별로 섹션을 나눠서 작성해주세요
```

### 예시 2: 법규 및 정책

**수동 실행 입력:**
```
키워드: 장애인차별금지법, ADA compliance, 유럽 접근성 법, EAA
추가 지시사항: 법률적 요구사항과 기업의 대응 방안을 중심으로 작성해주세요
```

### 예시 3: 도구 및 기술

**수동 실행 입력:**
```
키워드: axe-core, Lighthouse accessibility, NVDA updates, VoiceOver
추가 지시사항: 각 도구의 최신 기능과 사용법을 포함해주세요
```

## 📈 성능 및 비용

### 실행 시간
- **평균**: 2-3분
- **단계별**:
  - Setup: ~30초
  - 뉴스 수집: ~30초
  - Gemini API: ~60초
  - Commit/Push: ~30초

### GitHub Actions 사용량
- **무료 티어**: 월 2,000분
- **이 workflow**: 실행당 약 3분
- **주 1회 실행**: 월 12분 (0.6% 사용)
- **여유 충분**: 월 600회 이상 실행 가능!

### Gemini API 사용량
- **무료 티어**: 분당 15회, 일 1,500회 요청
- **이 workflow**: 실행당 1회 요청
- **주 1회 실행**: 월 4회 요청
- **여유 충분**: 할당량 걱정 없음!

## 🔄 통합 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│              accessibility_news.yml (이 파일)                 │
│  • 뉴스 수집 및 마크다운 생성                                   │
│  • 자동 커밋 & 푸시                                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ triggers on push to main
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                    deploy.yml (기존 파일)                     │
│  • Astro 빌드                                                 │
│  • GitHub Pages 배포                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ deploys to
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                       Live Website                           │
│  https://username.github.io/a11y-news                 │
└─────────────────────────────────────────────────────────────┘
```

## 🎭 실행 시나리오

### 시나리오 A: 정기 자동 실행

```bash
# 월요일 오전 9시(KST)가 되면...

[GitHub Actions]
  ✓ Schedule 트리거 발동
  ✓ 기본 키워드로 검색
  ✓ 약 15-25개 뉴스 수집
  ✓ Gemini로 요약 및 구조화
  ✓ a11y-news-2026-03-10.md 생성
  ✓ Git 커밋: "Add accessibility news for 2026-03-10"
  ✓ Push to main
  
[Deploy Workflow]
  ✓ Push 감지
  ✓ Astro 빌드
  ✓ GitHub Pages 배포
  
[결과]
  ✓ 블로그에 새 게시물 자동 게시!
```

### 시나리오 B: 긴급 뉴스 수동 수집

```bash
# W3C에서 WCAG 3.0이 발표된 당일

[사용자 액션]
  → GitHub Actions 탭 이동
  → Run workflow 클릭
  → 키워드: "WCAG 3.0, W3C Silver"
  → 추가 지시사항: "WCAG 3.0의 주요 변경사항을 상세히 다뤄주세요"
  → Run workflow 실행

[GitHub Actions]
  ✓ 입력된 키워드로 검색
  ✓ WCAG 3.0 관련 뉴스만 수집
  ✓ 커스텀 프롬프트 적용
  ✓ 전문적인 분석 포함된 게시물 생성
  ✓ 즉시 커밋 & 푸시
  
[결과]
  ✓ 3분 내 블로그에 전문 리포트 게시!
```

### 시나리오 C: 특정 주제 심층 분석

```bash
# 모바일 접근성 전문 게시물이 필요할 때

[사용자 액션]
  → Keywords: "mobile accessibility, iOS VoiceOver, Android TalkBack"
  → Custom Prompt: "모바일 앱 개발자를 위한 실용적인 가이드 형식으로 
                    작성하고, 코드 예제를 많이 포함해주세요"

[결과]
  ✓ 모바일 중심의 맞춤형 콘텐츠 생성!
```

## 🔗 파일 간 관계

```
.github/workflows/
├── accessibility_news.yml  ← 뉴스 수집 (이 파일)
│   └── triggers → deploy.yml
└── deploy.yml             ← GitHub Pages 배포 (기존)

scripts/
├── collect_news.py        ← 메인 스크립트
├── test_collection.py     ← 로컬 테스트용
└── README.md              ← 스크립트 문서

docs/
├── QUICKSTART.md          ← 5분 시작 가이드
├── AUTOMATION_GUIDE.md    ← 로컬 자동화 가이드
├── GITHUB_ACTIONS_GUIDE.md ← GitHub Actions 상세 가이드
└── WORKFLOW_ARCHITECTURE.md ← 이 문서
```

## 💡 베스트 프랙티스

### 1. 키워드 전략

**좋은 예:**
```
"WCAG 2.2", "accessibility compliance", "웹 접근성 인증"
```

**나쁜 예:**
```
"accessibility" (너무 광범위)
"WCAG 2.1.1.1.3.5.7" (너무 구체적)
```

### 2. 커스텀 프롬프트

**좋은 예:**
```
개발팀을 위한 실무 중심으로 작성하고, 
체크리스트를 포함해주세요
```

**나쁜 예:**
```
좋게 써줘 (구체적이지 않음)
```

### 3. 실행 빈도

| 목적 | 권장 빈도 | Cron |
|-----|----------|------|
| 일반 뉴스 아카이빙 | 주 1회 | `0 0 * * 1` |
| 중요 업데이트 모니터링 | 주 2회 | `0 0 * * 1,4` |
| 적극적 트래킹 | 매일 | `0 0 * * *` |

### 4. 중복 실행 방지

Workflow는 같은 날짜에 여러 번 실행되어도:
- ✅ 파일명이 날짜 기반이므로 덮어쓰기
- ✅ 최신 정보로 업데이트
- ✅ 중복 게시물 생성 안 함

## 🎓 학습 리소스

- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Cron 표현식 생성기](https://crontab.guru/)
- [Gemini API 문서](https://ai.google.dev/docs)

## 🤝 기여 및 피드백

워크플로우 개선 아이디어:
- [ ] Slack/Discord 알림 추가
- [ ] 실패 시 재시도 로직
- [ ] 수집된 뉴스 개수 배지 추가
- [ ] 여러 언어 지원
- [ ] 카테고리별 자동 분류

---

**자동화로 더 효율적인 뉴스 아카이빙을! 🚀**
