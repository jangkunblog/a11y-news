---
name: a11y-weekly
description: >
  웹 접근성(A11Y)과 디지털 포용에 관한 주간 뉴스 다이제스트를 자동 수집하고
  블로그 포스트로 발행합니다. 지난 한 주간의 접근성 관련 최신 소식을
  카테고리별로 정리합니다.
  "접근성 주간 뉴스", "a11y 다이제스트", "접근성 소식 정리" 등의 요청에 사용됩니다.
argument-hint: "[--team] [--draft] [--featured]"
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npm run *), Bash(git *), Task, WebSearch, WebFetch
---

# A11Y 주간 다이제스트 작성 & 발행

푸땡로그(Astro 5 + AstroPaper) 접근성 주간 뉴스 다이제스트 스킬입니다.
주제를 입력받지 않고, 지난 1주간의 접근성 뉴스를 5개 카테고리로 자동 수집합니다.

## 인자 파싱

`$ARGUMENTS`에서 파싱:
- `--team`: 4인 Agent Team으로 수집+작성+리뷰 병렬 수행
- `--draft`: 초안 상태 유지 (발행 안 함)
- `--featured`: 메인 페이지 고정

**주제 인자 없음** — 자동으로 "A11Y 주간 다이제스트: YYYY.MM.DD ~ MM.DD" 형태로 제목 생성

예시:
- `/a11y-weekly --draft`
- `/a11y-weekly --team`
- `/a11y-weekly --team --featured`

---

## Phase 1: 준비 & 중복 확인

1. 현재 날짜 기반으로 지난 1주 기간 산정 (예: 2026.03.01 ~ 2026.03.07)
   - 종료일: 오늘 (또는 가장 최근 일요일)
   - 시작일: 종료일 - 6일
2. slug 생성: `a11y-weekly-YYYY-MM-DD` (발행일 기준)
3. 파일 경로: `src/data/blog/a11y-weekly-YYYY-MM-DD.md`
4. `src/data/blog/` 내 `a11y-weekly-*` 패턴으로 기존 다이제스트 확인
5. 기존 포스트에서 이미 다룬 뉴스 항목(링크, 제목) 추출하여 중복 제거 목록 생성

---

## Phase 2: 팀 모드 vs 인라인 모드

### `--team` 플래그가 있을 때: Agent Team 생성

TeamCreate로 `a11y-weekly-[date]` 이름의 4인 팀을 구성한다.

#### 팀원 구성

**1. researcher-global (Explore 에이전트)**
- 카테고리 1(국내외 뉴스), 2(표준 업데이트), 3(도구 & 기술) 수집
- WebSearch/WebFetch로 지난 1주 이내 뉴스만 필터링
- 각 항목: 제목, 요약(2-3줄), 출처 링크, 날짜
- 기존 포스트에 포함된 링크/주제 제외
- 수집 결과를 writer에게 메시지로 전달

**2. researcher-local (Explore 에이전트)**
- 카테고리 4(법률 & 정책), 5(실무 사례 & 가이드) 수집
- 국내 뉴스 보강 (한국 접근성 관련 소식 중점)
- 수집 기준은 researcher-global과 동일
- 수집 결과를 writer에게 메시지로 전달

**3. writer (general-purpose 에이전트)**
- researcher-global과 researcher-local의 수집 결과를 통합
- `templates/weekly-digest-template.md` 템플릿 기반으로 포스트 작성
- `reference/sources.md`의 카테고리 가이드 참고
- `src/data/blog/a11y-weekly-[date].md` 파일 생성
- 초안 완성 후 reviewer에게 메시지로 알림

**4. reviewer (general-purpose 에이전트)**
- 뉴스 항목 정확성 검증 (링크 유효성, 날짜 확인)
- 기존 포스트와 중복 항목 최종 확인
- frontmatter 완전성 검증:
  - `title`, `pubDatetime`, `description` 필수 필드 확인
  - `description`이 160자 이내인지 확인
  - `tags` 소문자 일관성, 중복 없음
  - `slug` 형식 확인 (`a11y-weekly-YYYY-MM-DD`)
- `npm run build` 실행하여 빌드 성공 검증
- 발행 준비 상태를 팀 리더에게 보고

#### 태스크 의존성

```
researcher-global ─→ writer → reviewer
researcher-local  ─↗
```

#### 팀 워크플로우

1. TaskCreate로 각 팀원의 태스크를 생성하고 의존성(blockedBy) 설정
2. Task 도구로 각 팀원을 스폰 (team_name 파라미터 사용)
3. 팀원들이 자율적으로 태스크를 처리하고 서로 메시지 교환
4. 모든 태스크 완료 후 팀 리더가 최종 확인
5. shutdown_request로 팀원 종료 후 TeamDelete

### `--team` 플래그가 없을 때: 인라인 처리

Claude가 단독으로 순차 처리:
1. Phase 1 준비 & 중복 확인
2. 5개 카테고리별 WebSearch로 뉴스 수집
3. 수집 결과 통합 및 포스트 작성
4. 자체 검토 (정확성, 문체, frontmatter)
5. 빌드 검증
6. 발행

---

## Phase 3: 뉴스 수집 (5개 카테고리)

WebSearch/WebFetch로 카테고리별 수집. 검색 키워드는 `reference/sources.md` 참조.

| # | 카테고리 | 설명 |
|---|---------|------|
| 1 | 국내외 뉴스 | 접근성 관련 일반 뉴스, 기업/기관 동향 |
| 2 | 표준 업데이트 | WCAG, WAI-ARIA, W3C, ARIA APG 변경사항 |
| 3 | 도구 & 기술 | 접근성 테스트 도구, 스크린 리더, 라이브러리 업데이트 |
| 4 | 법률 & 정책 | 접근성 관련 법률, 소송, 정부 정책 |
| 5 | 실무 사례 & 가이드 | 접근성 구현 가이드, 모범 사례, 튜토리얼 |

### 수집 기준

- 지난 1주일 이내 뉴스만 포함
- 기존 포스트에 이미 포함된 링크/주제 제외
- 각 항목에 반드시 포함: **제목, 요약(2-3줄), 출처 링크, 날짜**
- 카테고리별 최소 1개, 최대 5개 항목 목표
- 해당 기간에 뉴스가 없는 카테고리는 "이번 주에는 주요 업데이트가 없었습니다." 로 표시

---

## Phase 4: 포스트 작성

### 파일 위치

`src/data/blog/a11y-weekly-YYYY-MM-DD.md`

**중요: `pubDatetime`에는 반드시 포스트 작성 시점의 현재 시간을 Asia/Seoul 기준 ISO 8601 형식으로 입력한다.**

### Frontmatter

```yaml
---
title: "A11Y 주간 다이제스트: YYYY.MM.DD ~ MM.DD"
author: 푸땡
pubDatetime: REPLACE_WITH_CURRENT_DATETIME  # 반드시 현재 시간(Asia/Seoul) ISO 8601
slug: a11y-weekly-YYYY-MM-DD
featured: false          # --featured 플래그로 결정
draft: true              # --draft 플래그로 결정, 기본 true
tags:
  - accessibility
  - a11y
  - 접근성
  - 주간-다이제스트
description: "YYYY.MM.DD ~ MM.DD 웹 접근성과 디지털 포용 관련 주간 뉴스 다이제스트"
timezone: "Asia/Seoul"
---
```

### 본문 구조

`templates/weekly-digest-template.md` 참조. 문체/컨벤션은 blog-post 스킬의 `reference/conventions.md` 동일 적용.

---

## Phase 5: 검증 & 발행

### 빌드 검증

```bash
npm run build
```

빌드 실패 시 에러를 분석하고 수정한다.

### 발행 처리

`--draft` 플래그가 없는 경우:
1. `draft: false`로 변경
2. `pubDatetime`을 현재 시간(Asia/Seoul)으로 업데이트
3. 커밋: `docs: "A11Y 주간 다이제스트: YYYY.MM.DD ~ MM.DD" 블로그 포스트 발행`
4. 사용자에게 push 여부 확인 후 진행

`--draft` 플래그가 있는 경우:
1. `draft: true` 유지
2. 커밋: `docs: "A11Y 주간 다이제스트: YYYY.MM.DD ~ MM.DD" 블로그 포스트 초안 작성`
3. push하지 않음

---

## 참고 정보

### 프로젝트 핵심 파일

| 파일 | 역할 |
|------|------|
| `src/content.config.ts` | Astro content collection 스키마 정의 |
| `src/config.ts` | SITE 설정 (author: "푸땡", lang: "ko", timezone: "Asia/Seoul") |
| `src/constants.ts` | Giscus 댓글, 소셜 링크, 공유 링크 설정 |
| `src/utils/postFilter.ts` | 초안/예약 포스트 필터링 |
| `src/utils/getSortedPosts.ts` | 날짜순 정렬 |

### 배포 파이프라인

- Netlify: main 브랜치 push 시 자동 배포
- 댓글: Giscus (kjy2143/blog-comments 리포지토리)
- OG 이미지: Satori + sharp로 빌드 시 자동 생성
