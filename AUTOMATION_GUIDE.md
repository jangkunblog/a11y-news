# 디지털 접근성 뉴스 자동 수집 가이드

이 문서는 Python 스크립트를 사용하여 자동으로 접근성 뉴스를 수집하고 블로그 게시물을 생성하는 방법을 설명합니다.

## 📋 사전 준비

### 1. Python 설치 확인

```bash
python --version  # Python 3.8 이상 필요
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Gemini API 키 발급

1. [Google AI Studio](https://aistudio.google.com/app/apikey)에 접속
2. "Create API Key" 버튼 클릭
3. API 키 복사

### 4. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일을 열고 API 키 입력:

```bash
GEMINI_API_KEY=your_actual_api_key_here
```

## 🚀 사용 방법

### 기본 실행

```bash
python scripts/collect_news.py
```

### 실행 결과

스크립트 실행 시:

1. **뉴스 수집**: Google News RSS에서 접근성 관련 뉴스 검색
2. **AI 요약**: Gemini API로 뉴스 요약 및 구조화
3. **마크다운 생성**: `src/content/blog/` 폴더에 날짜별 파일 생성
4. **자동 반영**: Astro 개발 서버가 실행 중이면 즉시 반영

### 생성되는 파일 형식

```
src/content/blog/a11y-news-2026-03-05.md
```

## 📝 생성되는 콘텐츠 구조

스크립트는 다음 규칙에 따라 콘텐츠를 생성합니다:

1. **요약(Summary) 섹션**: 전체 내용을 3-5문장으로 요약
2. **구조화된 본문**: 대제목, 소제목으로 체계적 구성
3. **출처 명시**: 모든 정보에 원문 링크 포함
4. **결론(Conclusion) 섹션**: 실무 적용 방안 및 전략 제시

## 🔍 검색 키워드 커스터마이징

`scripts/collect_news.py` 파일에서 검색 키워드를 수정할 수 있습니다:

```python
SEARCH_KEYWORDS = [
    "web accessibility WCAG",
    "digital accessibility standards",
    "ARIA accessibility",
    "웹 접근성",
    "디지털 접근성",
    # 원하는 키워드 추가
]
```

## ⚙️ 고급 설정

### Gemini 모델 변경

더 강력하거나 빠른 모델로 변경하려면:

```python
# scripts/collect_news.py의 generate_markdown_with_gemini 함수에서
model = genai.GenerativeModel('gemini-2.0-flash-exp')  # 현재 모델
# 또는
model = genai.GenerativeModel('gemini-pro')  # 다른 모델
```

### 수집 뉴스 개수 조정

```python
# collect_all_news 함수에서
articles = fetch_google_news(keyword, num_results=5)  # 5 -> 원하는 개수
```

## 🤖 자동화 설정

### 1. Cron Job (Linux/macOS)

매일 오전 9시에 자동 실행:

```bash
crontab -e
```

다음 라인 추가:

```
0 9 * * * cd /path/to/kakao-a11y-news && /usr/bin/python3 scripts/collect_news.py
```

### 2. GitHub Actions (CI/CD)

`.github/workflows/collect-news.yml` 파일 생성:

```yaml
name: Collect A11y News

on:
  schedule:
    - cron: '0 0 * * 1'  # 매주 월요일 자동 실행
  workflow_dispatch:  # 수동 실행 가능

jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Collect news
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python scripts/collect_news.py
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add src/content/blog/
          git commit -m "Add accessibility news $(date +%Y-%m-%d)" || exit 0
          git push
```

## 🔒 보안 주의사항

1. **.env 파일 관리**
   - `.env` 파일은 절대 Git에 커밋하지 마세요
   - `.gitignore`에 이미 포함되어 있습니다

2. **API 키 보호**
   - API 키를 코드에 하드코딩하지 마세요
   - GitHub Secrets 사용 (CI/CD 시)

## 🐛 문제 해결

### "GEMINI_API_KEY가 설정되지 않았습니다" 오류

- `.env` 파일이 프로젝트 루트에 있는지 확인
- API 키가 올바르게 입력되었는지 확인

### "수집된 뉴스가 없습니다" 오류

- 인터넷 연결 확인
- 검색 키워드를 더 일반적인 것으로 변경

### Gemini API 오류

- API 키가 유효한지 확인
- [Google AI Studio](https://aistudio.google.com/)에서 할당량 확인
- 무료 티어는 분당 요청 제한이 있을 수 있습니다

## 📚 참고 자료

- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google News RSS](https://support.google.com/news/answer/59255)

## 💡 팁

1. **정기적 실행**: 매주 또는 매일 자동으로 실행하도록 설정
2. **키워드 최적화**: 관심 있는 특정 기술이나 표준 추가
3. **수동 편집**: 생성된 마크다운 파일은 수동으로 편집 가능
4. **히어로 이미지**: 원하는 이미지로 변경 가능

## 🔄 업데이트 및 개선

스크립트 개선 아이디어:

- [ ] 다른 뉴스 소스 추가 (예: W3C 블로그, WebAIM)
- [ ] 중요도별 분류 기능
- [ ] 자동 번역 기능 (영문 -> 한글)
- [ ] 이메일 알림 기능
- [ ] Slack/Discord 웹훅 연동
