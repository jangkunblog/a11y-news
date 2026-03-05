# 🚀 GitHub 저장소 배포 가이드

이 가이드는 로컬 프로젝트를 https://github.com/jangkunblog/a11y-news.git 에 푸시하고 설정하는 방법을 안내합니다.

## 📤 1단계: GitHub에 푸시하기

### 옵션 A: HTTPS 사용 (권장)

```bash
# 1. 원격 저장소 추가 (이미 완료됨)
git remote add origin https://github.com/jangkunblog/a11y-news.git

# 2. GitHub에 로그인하여 푸시
git push -u origin main
```

푸시 시 GitHub 사용자명과 토큰을 입력하라는 메시지가 나타납니다.

#### Personal Access Token 생성 방법

1. GitHub.com > 우측 상단 프로필 클릭 > **Settings**
2. 좌측 하단 **Developer settings**
3. **Personal access tokens** > **Tokens (classic)**
4. **Generate new token** > **Generate new token (classic)**
5. 설정:
   - Note: `a11y-news-push`
   - Expiration: 90 days (또는 원하는 기간)
   - 권한 선택:
     - ✅ `repo` (전체 선택)
     - ✅ `workflow`
6. **Generate token** 클릭
7. 🔑 **생성된 토큰 복사** (다시 볼 수 없음!)

#### 푸시 실행

```bash
git push -u origin main

# Username: jangkunblog
# Password: [복사한 Personal Access Token 붙여넣기]
```

### 옵션 B: SSH 사용

```bash
# 1. 원격 저장소를 SSH로 변경
git remote set-url origin git@github.com:jangkunblog/a11y-news.git

# 2. SSH 키가 없다면 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# 3. SSH 키를 GitHub에 등록
# GitHub.com > Settings > SSH and GPG keys > New SSH key
# ~/.ssh/id_ed25519.pub 내용 복사하여 붙여넣기

# 4. 푸시
git push -u origin main
```

---

## ⚙️ 2단계: GitHub Pages 설정

푸시가 완료되면:

1. GitHub 저장소 페이지 이동: https://github.com/jangkunblog/a11y-news
2. **Settings** 탭 클릭
3. 좌측 메뉴에서 **Pages** 클릭
4. **Source** 설정:
   - ✅ **GitHub Actions** 선택 (Source 드롭다운)
5. Save

### base 경로 활성화

`astro.config.mjs` 파일을 수정하여 GitHub Pages 경로 활성화:

```javascript
export default defineConfig({
	site: 'https://jangkunblog.github.io',
	base: '/a11y-news',  // 이 줄의 주석 해제
	integrations: [mdx(), sitemap()],
});
```

커밋 및 푸시:

```bash
git add astro.config.mjs
git commit -m "Enable base path for GitHub Pages"
git push
```

약 1-2분 후 **https://jangkunblog.github.io/a11y-news** 에서 블로그 확인 가능!

---

## 🔐 3단계: GitHub Secrets 설정 (자동화용)

자동 뉴스 수집 기능을 사용하려면:

1. 저장소 페이지 > **Settings** 탭
2. **Secrets and variables** > **Actions**
3. **New repository secret** 클릭
4. Secret 추가:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: [Gemini API 키 붙여넣기]
5. **Add secret** 클릭

### Gemini API 키 발급 방법

1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정 로그인
3. **Create API Key** 클릭
4. API 키 복사
5. GitHub Secrets에 등록

---

## ✅ 4단계: GitHub Actions 권한 설정

1. 저장소 > **Settings** > **Actions** > **General**
2. **Workflow permissions** 섹션:
   - ✅ **Read and write permissions** 선택
   - ✅ **Allow GitHub Actions to create and approve pull requests** 선택
3. **Save** 클릭

이 설정이 있어야 자동 수집 스크립트가 생성된 파일을 커밋할 수 있습니다.

---

## 🧪 5단계: 테스트

### GitHub Actions 수동 실행 테스트

1. 저장소 > **Actions** 탭
2. 좌측에서 **"Collect Accessibility News"** 클릭
3. **Run workflow** 버튼 클릭
4. 입력:
   - Branch: `main`
   - 검색 키워드: (비워둠 - 기본 키워드 사용)
   - 추가 지시사항: (비워둠)
5. **Run workflow** 클릭

약 2-3분 후:
- ✅ Workflow 완료 확인
- ✅ `src/content/blog/` 폴더에 새 파일 생성 확인
- ✅ 자동 커밋 확인
- ✅ Deploy workflow 자동 실행 확인

### GitHub Pages 확인

약 1-2분 후 **https://jangkunblog.github.io/a11y-news** 접속하여 블로그 확인!

---

## 📋 설정 체크리스트

완료한 항목을 체크하세요:

### 기본 설정
- [ ] GitHub에 코드 푸시 완료
- [ ] GitHub Pages Source를 "GitHub Actions"로 설정
- [ ] `astro.config.mjs`의 base 주석 해제 및 푸시
- [ ] 블로그 사이트 접속 확인 (https://jangkunblog.github.io/a11y-news)

### 자동화 설정
- [ ] Gemini API 키 발급
- [ ] GitHub Secrets에 GEMINI_API_KEY 등록
- [ ] Actions 권한을 "Read and write" 설정
- [ ] Actions 탭에서 수동 실행 테스트
- [ ] 생성된 게시물 확인

### 정기 실행 확인
- [ ] 다음 월요일 오전 9시까지 대기
- [ ] 자동 실행 결과 확인
- [ ] 블로그에 새 게시물 자동 게시 확인

---

## 🔧 Git 원격 저장소 설정

현재 상태:

```bash
# 이미 완료됨
git remote add origin https://github.com/jangkunblog/a11y-news.git
git branch -M main
```

남은 작업:

```bash
# 푸시만 하면 됩니다
git push -u origin main
```

---

## 🌐 최종 URL

설정 완료 후 다음 URL에서 접근 가능합니다:

| 항목 | URL |
|------|-----|
| 🏠 블로그 홈 | https://jangkunblog.github.io/a11y-news |
| 📝 블로그 목록 | https://jangkunblog.github.io/a11y-news/blog |
| ℹ️ 소개 페이지 | https://jangkunblog.github.io/a11y-news/about |
| 📡 RSS Feed | https://jangkunblog.github.io/a11y-news/rss.xml |
| 🗺️ Sitemap | https://jangkunblog.github.io/a11y-news/sitemap-index.xml |

---

## 🐛 문제 해결

### "fatal: could not read Username"

**원인**: GitHub 인증 필요

**해결**: Personal Access Token 생성 (위 가이드 참조)

### "Permission denied (publickey)"

**원인**: SSH 키 미등록

**해결**: 
- 옵션 A 사용 (HTTPS)
- 또는 SSH 키 생성 및 등록

### "403 Forbidden"

**원인**: 저장소 권한 없음 또는 토큰 권한 부족

**해결**:
- 저장소 소유자 확인
- 토큰 권한에 `repo` 포함 확인

### 배포 후 404 오류

**원인**: base 경로 미설정

**해결**: `astro.config.mjs`에서 `base: '/a11y-news'` 주석 해제

---

## 📞 다음 단계

1. ✅ **지금 바로**: 위 가이드대로 GitHub에 푸시
2. ✅ **5분 후**: GitHub Pages 설정 및 확인
3. ✅ **10분 후**: Gemini API 키 등록 및 Actions 테스트
4. ✅ **다음 월요일**: 자동 뉴스 수집 확인!

---

**모든 준비가 완료되었습니다! 이제 푸시만 하면 됩니다! 🚀**
