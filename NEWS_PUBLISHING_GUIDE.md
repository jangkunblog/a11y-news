# 📰 뉴스 발행 가이드

디지털 접근성 뉴스 자동 수집 및 발행 시스템 완전 가이드

---

## 🎯 시스템 개요

이 시스템은 **Pull Request 기반 검토 프로세스**를 사용합니다:

```
뉴스 수집 → PR 생성 → 검토 → Merge → 자동 배포
```

**장점**:
- ✅ 발행 전 내용 검토 가능
- ✅ 필요시 직접 수정 가능
- ✅ 승인 후에만 블로그에 발행
- ✅ 변경 이력 추적 용이

---

## 📋 목차

1. [자동 발행 (매주 월요일)](#1-자동-발행-매주-월요일)
2. [수동 테스트 발행 (지금 바로)](#2-수동-테스트-발행-지금-바로)
3. [특정 주제로 비정기 발행](#3-특정-주제로-비정기-발행)
4. [Pull Request 검토 및 발행](#4-pull-request-검토-및-발행)
5. [게시물 수정하기](#5-게시물-수정하기)
6. [동일한 날짜 여러 게시물 발행](#6-동일한-날짜-여러-게시물-발행)
7. [문제 해결](#7-문제-해결)

---

## 1. 자동 발행 (매주 월요일)

### ⏰ 실행 시간
**매주 월요일 오전 9시 (KST)** 자동 실행

### 🔄 자동 프로세스

```
월요일 오전 9시
    ↓
뉴스 자동 수집
    ↓
Gemini AI 요약 & 구조화
    ↓
Pull Request 자동 생성 ✨
    ↓
이메일/알림 수신
    ↓
[수동] PR 검토 & Merge
    ↓
블로그 자동 배포
```

### ✅ 필수 설정

1. **Gemini API 키 등록**
   - https://github.com/jangkunblog/a11y-news/settings/secrets/actions
   - **New repository secret** 클릭
   - Name: `GEMINI_API_KEY`
   - Secret: [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급
   - **Add secret** 클릭

2. **Actions 권한 설정**
   - https://github.com/jangkunblog/a11y-news/settings/actions
   - **Workflow permissions** 섹션
   - ✅ **Read and write permissions** 선택
   - **Save** 클릭

3. **PR 알림 받기** (선택사항)
   - GitHub 프로필 > Settings > Notifications
   - "Pull requests" 알림 활성화
   - 이메일 또는 모바일 앱으로 알림 수신

---

## 2. 수동 테스트 발행 (지금 바로)

### 🚀 "알아서 중요 주제"로 테스트 발행

1. **Actions 페이지로 이동**
   ```
   https://github.com/jangkunblog/a11y-news/actions
   ```

2. **워크플로우 선택**
   - 좌측 메뉴에서 **"Collect Accessibility News"** 클릭

3. **수동 실행**
   - 우측 상단 **"Run workflow"** 버튼 클릭
   - 드롭다운 메뉴가 나타남

4. **기본값으로 실행**
   - 모든 입력 필드를 **비워둠** (기본 키워드 사용)
   - 초록색 **"Run workflow"** 버튼 클릭

5. **진행 상황 확인**
   - 워크플로우 실행 목록에 새 항목 생성
   - 클릭하여 실시간 로그 확인
   - 약 2-3분 소요

6. **PR 확인**
   - 완료 후 [Pull Requests 탭](https://github.com/jangkunblog/a11y-news/pulls) 확인
   - "📰 디지털 접근성 뉴스 - YYYY-MM-DD" PR 생성됨

---

## 3. 특정 주제로 비정기 발행

### 🎯 커스텀 키워드로 발행

**예시 시나리오**: "AI 접근성"에 관한 뉴스만 수집하고 싶을 때

1. **Actions 페이지로 이동**
   ```
   https://github.com/jangkunblog/a11y-news/actions
   ```

2. **워크플로우 선택**
   - "Collect Accessibility News" 클릭

3. **Run workflow 클릭**

4. **키워드 입력**
   - **"검색할 키워드 (쉼표로 구분)"** 필드에 입력
   
   ```
   예시 1: AI 접근성, 인공지능 웹접근성
   예시 2: WCAG 3.0, W3C 업데이트
   예시 3: 모바일 접근성, 안드로이드 TalkBack
   ```

5. **추가 지시사항** (선택사항)
   - **"Gemini에 전달할 추가 지시사항"** 필드
   
   ```
   예시 1: 기술적인 내용보다 법규/정책 중심으로 정리해줘
   예시 2: 개발자보다 기획자 관점에서 작성해줘
   예시 3: 실무 적용 사례 위주로 요약해줘
   ```

6. **실행**
   - **"Run workflow"** 버튼 클릭

### 📅 활용 예시

| 상황 | 키워드 예시 |
|------|------------|
| 특정 기술 조사 | `ARIA 2.0, WAI-ARIA 업데이트` |
| 법규 변경 확인 | `접근성 법규, 장애인차별금지법` |
| 특정 플랫폼 | `iOS VoiceOver, 애플 접근성` |
| 특정 업체 | `구글 접근성, 마이크로소프트 인클루시브` |
| 이벤트/컨퍼런스 | `접근성 컨퍼런스, a11y meetup` |

---

## 4. Pull Request 검토 및 발행

### 🔍 PR 검토 프로세스

#### A. PR 찾기

1. **Pull Requests 탭으로 이동**
   ```
   https://github.com/jangkunblog/a11y-news/pulls
   ```

2. **최신 PR 확인**
   - "📰 디지털 접근성 뉴스 - YYYY-MM-DD" 제목
   - `github-actions[bot]`이 생성
   - 초록색 "Open" 상태

#### B. 내용 검토

1. **PR 클릭**하여 상세 페이지 진입

2. **"Files changed" 탭** 클릭
   - 생성된 마크다운 파일 내용 확인
   - 빨간색/초록색으로 변경 사항 표시

3. **체크리스트 확인**
   - [ ] 뉴스 내용이 정확하고 적절한가?
   - [ ] 출처 링크가 모두 포함되어 있는가?
   - [ ] 요약과 결론이 명확한가?
   - [ ] 오타나 문법 오류가 없는가?

#### C. 승인 및 발행

**✅ 내용이 만족스러운 경우:**

1. **"Conversation" 탭**으로 돌아가기
2. 하단의 **"Merge pull request"** 버튼 클릭
3. **"Confirm merge"** 클릭
4. ✨ **자동으로 Vercel 배포 시작!**
5. 약 1-2분 후 블로그에서 확인 가능

**❌ 내용이 부적절한 경우:**

1. **"Close pull request"** 버튼 클릭
2. PR이 닫히고 게시물은 발행되지 않음

---

## 5. 게시물 수정하기

PR 검토 중 수정이 필요한 경우:

### 방법 1: GitHub 웹에서 직접 수정 (간단)

1. **Files changed** 탭에서 수정할 파일 찾기
2. 파일명 우측 **"..."** 메뉴 클릭
3. **"Edit file"** 선택
4. 내용 수정
5. 하단 **"Commit changes"** 클릭
6. "Commit directly to the `news/YYYY-MM-DD-HHMMSS` branch" 선택
7. **"Commit changes"** 확인
8. 자동으로 PR에 반영됨

### 방법 2: 로컬에서 수정 (고급)

```bash
# 브랜치 가져오기 (시간 포함 브랜치명)
git fetch origin
git checkout news/YYYY-MM-DD-HHMMSS

# 파일 수정 (시간 포함 파일명)
code src/content/blog/a11y-news-YYYY-MM-DD-HHMMSS.md

# 커밋 및 푸시
git add .
git commit -m "게시물 내용 수정"
git push

# PR에 자동 반영됨
```

---

## 6. 동일한 날짜 여러 게시물 발행

### 🎯 지원 기능

시스템은 **같은 날짜에 여러 개의 뉴스 게시물**을 발행할 수 있습니다.

### 📝 작동 방식

**파일명 형식**: `a11y-news-YYYY-MM-DD-HHMMSS.md`

- 날짜 + 시간(시분초)으로 고유한 파일명 생성
- 예시:
  - `a11y-news-2026-03-05-090000.md` (오전 9시)
  - `a11y-news-2026-03-05-140000.md` (오후 2시)
  - `a11y-news-2026-03-05-185839.md` (오후 6시 58분 39초)

**브랜치명 형식**: `news/YYYY-MM-DD-HHMMSS`

- 각 실행마다 고유한 브랜치 생성
- 예시: `news/2026-03-05-090000`

**게시물 정렬**: 

- `pubDate`에 시간이 포함되어 자동으로 시간순 정렬
- 나중에 발행한 게시물이 먼저 표시됨

### 🔄 사용 시나리오

1. **아침**: "WCAG 업데이트" 주제로 발행
   ```
   → 파일: a11y-news-2026-03-05-090000.md
   → 브랜치: news/2026-03-05-090000
   → PR: "📰 디지털 접근성 뉴스 - 2026-03-05 09:00:00"
   ```

2. **오후**: "AI 접근성" 주제로 추가 발행
   ```
   → 파일: a11y-news-2026-03-05-140000.md
   → 브랜치: news/2026-03-05-140000
   → PR: "📰 디지털 접근성 뉴스 - 2026-03-05 14:00:00"
   ```

3. **결과**: 두 게시물 모두 블로그에 표시 (시간순 정렬)

### ⚠️ 주의사항

- 각 실행마다 **별도의 PR**이 생성됩니다
- PR을 검토하고 Merge할 때 **순서에 주의**하세요
- 먼저 발행하고 싶은 것부터 Merge하면 됩니다

---

## 7. 문제 해결

### 🐛 일반적인 문제

#### Q1. PR이 생성되지 않아요

**확인 사항:**
- Actions 워크플로우가 성공적으로 완료되었나요?
  - https://github.com/jangkunblog/a11y-news/actions
  - 실패 시 빨간색 X 표시, 로그 확인 필요
- `GEMINI_API_KEY`가 올바르게 설정되어 있나요?
- Actions 권한이 "Read and write permissions"로 설정되어 있나요?

#### Q2. 워크플로우가 실패해요

**가능한 원인:**
1. **Gemini API 키 오류**
   - Settings > Secrets > Actions에서 키 재확인
   - [Google AI Studio](https://aistudio.google.com/app/apikey)에서 새 키 발급

2. **Python 패키지 오류**
   - `requirements.txt` 파일 확인
   - 버전 호환성 문제일 수 있음

3. **네트워크 오류**
   - 일시적 문제일 수 있음
   - "Re-run failed jobs" 버튼으로 재실행

#### Q3. 뉴스가 수집되지 않아요

**가능한 원인:**
- 검색 키워드에 맞는 뉴스가 실제로 없을 수 있음
- 키워드를 더 일반적으로 변경해보세요
- 예: "WCAG 3.0" → "웹 접근성", "WCAG"

#### Q4. Merge 후 블로그에 표시되지 않아요

**확인 사항:**
1. Vercel 배포 상태 확인
   - https://app.netlify.com
   - 사이트 선택 > Deploys 탭
   - 최근 배포가 "Published" 상태인지 확인

2. 브라우저 캐시 삭제
   - Cmd+Shift+R (Mac) 또는 Ctrl+Shift+R (Windows)
   - 하드 리프레시

3. 파일 위치 확인
   - `src/content/blog/` 폴더에 파일이 있는지 확인

---

## 🎓 사용 시나리오

### 시나리오 1: 정기 발행 (매주)

```
월요일 아침 → 이메일/알림 수신
           → GitHub PR 페이지 접속
           → 내용 검토 (2-3분)
           → Merge 버튼 클릭
           → 완료! 🎉
```

**소요 시간**: 5분 이내

---

### 시나리오 2: 긴급 주제 발행

```
중요 뉴스 발견 (예: WCAG 3.0 발표)
    → Actions에서 수동 실행
    → 키워드: "WCAG 3.0, W3C 발표"
    → 2-3분 대기
    → PR 검토 & Merge
    → 블로그에 즉시 반영
```

**소요 시간**: 10분 이내

---

### 시나리오 3: 월간 리포트

```
매월 말일
    → Actions 수동 실행
    → 키워드: "접근성 월간 리포트"
    → 추가 지시: "이번 달 주요 동향 정리"
    → PR 생성
    → 내용 확인 및 보완
    → Merge
```

---

## 📞 추가 도움말

### 유용한 링크

- 📚 [GitHub Actions 가이드](./GITHUB_ACTIONS_GUIDE.md)
- 🚀 [배포 가이드](./DEPLOYMENT_GUIDE.md)
- 🤖 [자동화 가이드](./AUTOMATION_GUIDE.md)
- ⚙️ [워크플로우 아키텍처](./WORKFLOW_ARCHITECTURE.md)

### 연락처

- 저장소 이슈: https://github.com/jangkunblog/a11y-news/issues
- 디스커션: https://github.com/jangkunblog/a11y-news/discussions

---

## 🎯 요약

| 작업 | 방법 | 소요 시간 |
|------|------|----------|
| 자동 발행 (매주) | PR 검토 & Merge만 | 5분 |
| 수동 테스트 | Actions > Run workflow | 10분 |
| 특정 주제 발행 | Actions > 키워드 입력 | 10분 |
| 내용 수정 | PR에서 직접 수정 | 5분 |

---

**💡 핵심**: 이제 모든 게시물은 **PR로 검토 후 발행**되므로, 품질 관리가 가능합니다!
