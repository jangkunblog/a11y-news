# 🚀 Netlify 배포 가이드

## 📋 준비 완료 사항
- ✅ `netlify.toml` 설정 파일 생성
- ✅ `astro.config.mjs` Netlify용으로 수정
- ✅ 로컬 커밋 완료

---

## 🔥 Netlify 배포 단계 (5분)

### 1단계: GitHub에 푸시

터미널에서 실행:

```bash
git push
```

---

### 2단계: Netlify 계정 생성 및 로그인

1. **Netlify 사이트 접속**: https://app.netlify.com
2. **"Sign up"** 클릭
3. **"GitHub"** 버튼으로 로그인 (GitHub 계정 사용)
4. GitHub 인증 허용

---

### 3단계: 새 사이트 생성

1. Netlify 대시보드에서 **"Add new site"** 클릭
2. **"Import an existing project"** 선택
3. **"Deploy with GitHub"** 선택
4. GitHub 인증 (처음 한 번만)
5. 저장소 검색: **"a11y-news"** 입력
6. **"jangkunblog/a11y-news"** 선택

---

### 4단계: 빌드 설정 확인

자동으로 감지될 것입니다:

- **Branch to deploy**: `main`
- **Build command**: `npm run build`
- **Publish directory**: `dist`

> ✅ `netlify.toml` 파일 덕분에 자동 설정됩니다!

**"Deploy site"** 버튼 클릭!

---

### 5단계: 배포 완료 대기 (1-2분)

1. 빌드 로그 자동 표시
2. ✅ "Published" 상태 확인
3. 생성된 URL 확인 (예: `https://random-name-123456.netlify.app`)

---

### 6단계: 사이트 이름 변경 (선택)

1. **Site settings** 클릭
2. **"Change site name"** 클릭
3. 원하는 이름 입력 (예: `a11y-news-blog`)
4. **Save**

최종 URL: `https://a11y-news-blog.netlify.app`

---

## 🤖 GitHub Actions 자동화 연동

**중요**: GitHub Actions는 그대로 작동합니다!

1. 뉴스 수집 스크립트가 매주 실행됨
2. GitHub 저장소에 새 마크다운 파일 추가
3. **Netlify가 자동으로 변경 감지**
4. **자동 재배포!** 🎉

---

## ⚙️ Gemini API 키 설정 (GitHub에서)

Netlify가 아니라 **GitHub Secrets**에 설정합니다 (이미 설명드린 방법):

1. https://github.com/jangkunblog/a11y-news/settings/secrets/actions
2. **New repository secret**
3. Name: `GEMINI_API_KEY`
4. Secret: [Google AI Studio에서 발급](https://aistudio.google.com/app/apikey)
5. **Add secret**

---

## 🔧 Actions 권한 설정

1. https://github.com/jangkunblog/a11y-news/settings/actions
2. **Workflow permissions**
3. ✅ **"Read and write permissions"** 선택
4. **Save**

---

## 🌐 최종 결과

### 배포 URL
- 🌍 **Netlify**: `https://your-site-name.netlify.app`
- 📦 **GitHub**: `https://github.com/jangkunblog/a11y-news`

### 자동화 흐름
```
매주 월요일 오전 9시
    ↓
GitHub Actions 실행
    ↓
뉴스 수집 & 마크다운 생성
    ↓
GitHub 저장소 커밋
    ↓
Netlify 자동 감지
    ↓
자동 재배포
    ↓
✨ 새 글 게시 완료!
```

---

## 🎯 체크리스트

```
로컬 작업
  ✅ netlify.toml 생성
  ✅ astro.config.mjs 수정
  ✅ Git 커밋
  ⏳ Git push

Netlify 설정
  ⏳ 계정 생성/로그인
  ⏳ 저장소 연결
  ⏳ 배포 완료
  ⏳ 사이트 이름 변경

GitHub 자동화
  ⏳ Gemini API 키 등록
  ⏳ Actions 권한 설정
  ⏳ 수동 테스트 실행
```

---

## 💡 다음 단계

1. **지금 바로**: `git push` 실행
2. **그 다음**: 위 2단계부터 Netlify 설정 시작!

궁금한 점이나 막히는 부분이 있으면 언제든 물어보세요! 🚀
