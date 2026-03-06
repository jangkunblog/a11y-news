# 디지털 접근성 뉴스

웹 접근성과 디지털 포용에 관한 최신 뉴스와 업데이트를 아카이빙하는 블로그입니다.

## 🚀 프로젝트 구조

```
/
├── public/              # 정적 파일 (favicon, fonts, images)
├── src/
│   ├── components/      # Astro 컴포넌트
│   ├── content/
│   │   └── blog/       # 블로그 게시물 (마크다운 파일)
│   ├── layouts/        # 레이아웃 템플릿
│   ├── pages/          # 페이지 라우트
│   └── styles/         # 글로벌 스타일
├── astro.config.mjs    # Astro 설정
└── package.json
```

## 📝 새 게시물 작성하기

1. `src/content/blog/` 폴더에 새 마크다운 파일 생성
2. 프론트매터 작성:

```markdown
---
title: '게시물 제목'
description: '게시물 설명'
pubDate: 'Mar 05 2026'
heroImage: '../../assets/your-image.jpg'
---

게시물 내용...
```

3. 파일 저장 시 자동으로 블로그에 표시됩니다

## 🤖 자동 뉴스 수집

### 로컬 실행

Python 스크립트를 사용하여 디지털 접근성 관련 뉴스를 자동으로 수집하고 블로그 게시물을 생성할 수 있습니다.

#### 설정 방법

1. Python 의존성 설치:
```bash
pip install -r requirements.txt
```
   - 뉴스 수집은 **googlesearch-python**(무료)을 사용합니다. 별도 검색 API 키 설정은 필요 없습니다.

2. Gemini API 키 설정:
```bash
cp .env.example .env
# .env 파일을 열어 GEMINI_API_KEY 입력
```

3. 스크립트 실행:
```bash
python scripts/collect_news.py

# 또는 커스텀 키워드로 실행
python scripts/collect_news.py --keywords "WCAG 3.0" "ARIA updates"
```

자세한 사용법은 [QUICKSTART.md](./QUICKSTART.md)를 참고하세요.

### GitHub Actions 자동화 ⭐

**매주 월요일 오전 9시(KST)**에 자동으로 뉴스를 수집하고 커밋합니다!

#### 설정 방법

1. [Google AI Studio](https://aistudio.google.com/app/apikey)에서 Gemini API 키 발급
2. GitHub 저장소 Settings > Secrets and variables > Actions
3. New repository secret:
   - Name: `GEMINI_API_KEY`
   - Secret: 발급받은 API 키
4. Settings > Actions > General > Workflow permissions
   - "Read and write permissions" 선택

#### 수동 실행

GitHub 저장소 > **Actions** 탭 > **"Collect Accessibility News"** > **Run workflow**

- 검색 키워드 커스터마이징 가능
- Gemini에 추가 지시사항 전달 가능

자세한 내용은 [GITHUB_ACTIONS_GUIDE.md](./GITHUB_ACTIONS_GUIDE.md)를 참고하세요.

## 🧞 명령어

프로젝트 루트에서 실행 가능한 명령어:

| 명령어                | 설명                                      |
| :-------------------- | :---------------------------------------- |
| `npm install`         | 의존성 설치                               |
| `npm run dev`         | 개발 서버 시작 (`localhost:4321`)         |
| `npm run build`       | 프로덕션 빌드 (`./dist/`)                 |
| `npm run preview`     | 빌드 미리보기                             |

## 🌐 GitHub Pages 배포

### 초기 설정

1. GitHub에 저장소 생성
2. `astro.config.mjs`의 `site`와 `base` 수정:

```javascript
export default defineConfig({
  site: 'https://yourusername.github.io',
  base: '/repository-name',
  // ...
});
```

3. 저장소 Settings > Pages에서:
   - Source: GitHub Actions 선택

### 배포

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/repository-name.git
git push -u origin main
```

push 시 자동으로 GitHub Actions가 실행되어 배포됩니다.

## ♿ 접근성 기능

이 블로그는 WCAG 2.1 AA 수준의 접근성 표준을 준수합니다:

- ✅ 시맨틱 HTML 사용
- ✅ 적절한 헤딩 구조
- ✅ 키보드 탐색 지원
- ✅ 포커스 표시 명확화
- ✅ 충분한 색상 대비
- ✅ 반응형 디자인
- ✅ 스크린 리더 지원

## 🛠️ 기술 스택

- [Astro](https://astro.build/) - 정적 사이트 생성기
- [MDX](https://mdxjs.com/) - 마크다운 + JSX
- [Sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/) - 자동 사이트맵 생성
- [RSS](https://docs.astro.build/en/guides/rss/) - RSS 피드 지원

## 📚 참고 자료

- [Astro 문서](https://docs.astro.build)
- [WCAG 2.1 가이드라인](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN 접근성 문서](https://developer.mozilla.org/ko/docs/Web/Accessibility)

## 📄 라이선스

MIT

## 🤝 기여

접근성 관련 뉴스나 개선 제안이 있으시면 이슈나 PR을 열어주세요!
