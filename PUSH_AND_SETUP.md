# 🎯 빠른 배포 가이드

## 현재 상태 ✅

- ✅ 프로젝트 폴더: `a11y-news` (변경 완료)
- ✅ Git 저장소 초기화 완료
- ✅ 원격 저장소 연결: `https://github.com/jangkunblog/a11y-news.git`
- ✅ 모든 파일에서 "kakao" 제거 완료
- ✅ 로컬 개발 서버 실행 중: http://localhost:4321

---

## 🚀 지금 바로 할 일

### 1단계: GitHub에 푸시 (2분)

터미널에서 실행:

```bash
git push -u origin main
```

**인증 필요 시**:
- Username: `jangkunblog`
- Password: `Personal Access Token` (아래 참조)

#### 🔑 Personal Access Token 발급

GitHub 비밀번호 대신 토큰이 필요합니다:

1. https://github.com/settings/tokens 접속
2. **Generate new token** > **Generate new token (classic)**
3. 설정:
   - Note: `a11y-news-deploy`
   - Expiration: 90 days
   - 권한: ✅ `repo`, ✅ `workflow`
4. 생성 후 **토큰 복사** 🔐
5. 푸시 시 Password에 붙여넣기

---

### 2단계: GitHub Pages 활성화 (1분)

푸시 후 즉시:

1. https://github.com/jangkunblog/a11y-news/settings/pages
2. **Source**: **GitHub Actions** 선택
3. 완료! (자동 저장됨)

---

### 3단계: base 경로 활성화 (1분)

`astro.config.mjs` 파일 수정:

```bash
# 주석 해제
sed -i '' 's|// base:|base:|' astro.config.mjs

# 확인
cat astro.config.mjs

# 커밋 및 푸시
git add astro.config.mjs
git commit -m "Enable base path for GitHub Pages"
git push
```

**약 1-2분 후**: https://jangkunblog.github.io/a11y-news 접속 가능! 🎉

---

### 4단계: 자동화 설정 (5분)

#### A. Gemini API 키 발급

1. https://aistudio.google.com/app/apikey 접속
2. **Create API Key** 클릭
3. API 키 복사 📋

#### B. GitHub Secrets 등록

1. https://github.com/jangkunblog/a11y-news/settings/secrets/actions
2. **New repository secret**
3. 입력:
   - Name: `GEMINI_API_KEY`
   - Secret: [복사한 API 키]
4. **Add secret**

#### C. Actions 권한 설정

1. https://github.com/jangkunblog/a11y-news/settings/actions
2. **Workflow permissions**:
   - ✅ **Read and write permissions** 선택
3. **Save**

---

### 5단계: 테스트 실행 (3분)

1. https://github.com/jangkunblog/a11y-news/actions
2. 좌측 **"Collect Accessibility News"** 클릭
3. **Run workflow** 클릭
4. **Run workflow** 버튼 클릭 (기본값 사용)
5. 2-3분 대기
6. ✅ 성공 확인!

---

## 📋 전체 체크리스트

```
기본 배포
  ✅ Git push 완료
  ✅ GitHub Pages 활성화
  ✅ base 경로 설정 및 푸시
  ✅ 블로그 접속 확인 (https://jangkunblog.github.io/a11y-news)

자동화 설정
  ✅ Gemini API 키 발급
  ✅ GitHub Secrets 등록
  ✅ Actions 권한 설정
  ✅ 수동 실행 테스트
  ✅ 생성된 게시물 확인

정기 실행
  ✅ 매주 월요일 오전 9시 자동 실행 대기
```

---

## 🌐 최종 URL

| 서비스 | URL |
|--------|-----|
| 📝 블로그 | https://jangkunblog.github.io/a11y-news |
| 💻 저장소 | https://github.com/jangkunblog/a11y-news |
| ⚙️ Actions | https://github.com/jangkunblog/a11y-news/actions |

---

## ⚡ 요약: 3개 명령어로 완성

```bash
# 1. 푸시
git push -u origin main

# 2. base 활성화 & 푸시
sed -i '' 's|// base:|base:|' astro.config.mjs && \
git add astro.config.mjs && \
git commit -m "Enable base path for GitHub Pages" && \
git push

# 3. GitHub 웹사이트에서 Settings 3개 설정
#    - Pages: GitHub Actions 선택
#    - Secrets: GEMINI_API_KEY 등록
#    - Actions: Read and write 권한
```

**5분 후 완성! 🎉**

---

## 💡 자동화 동작 방식

설정 완료 후:

```
매주 월요일 오전 9시(KST)
         ↓
GitHub Actions 자동 실행
         ↓
접근성 뉴스 수집
         ↓
Gemini AI 요약 & 구조화
         ↓
마크다운 파일 생성
         ↓
자동 커밋 & 푸시
         ↓
블로그 자동 배포
         ↓
✨ 새 게시물 게시 완료!
```

**아무것도 하지 않아도 매주 새 글이 올라옵니다!** 🚀

---

자세한 내용은:
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - 상세 배포 가이드
- [GITHUB_ACTIONS_GUIDE.md](./GITHUB_ACTIONS_GUIDE.md) - Actions 설정
