# 자동화 스크립트

이 폴더는 디지털 접근성 뉴스를 자동으로 수집하고 블로그 게시물을 생성하는 Python 스크립트를 포함합니다.

## 📁 파일 구조

```
scripts/
├── collect_news.py      # 메인 뉴스 수집 스크립트
├── test_collection.py   # 테스트 스크립트 (API 키 불필요)
└── README.md           # 이 파일
```

## 🚀 빠른 시작

### 1. 테스트 (API 키 없이)

```bash
python scripts/test_collection.py
```

뉴스 수집 기능이 정상 작동하는지 확인합니다.

### 2. 실제 실행

```bash
# .env 파일 설정 후
python scripts/collect_news.py
```

## 🔧 스크립트 상세

### collect_news.py

**기능:**
- Google News RSS에서 접근성 관련 뉴스 검색
- Gemini API로 뉴스 요약 및 구조화
- 마크다운 블로그 게시물 자동 생성

**필수 환경 변수:**
- `GEMINI_API_KEY`: Google Gemini API 키

**생성 파일:**
- `src/content/blog/a11y-news-YYYY-MM-DD.md`

**검색 키워드:**
- web accessibility WCAG
- digital accessibility standards
- ARIA accessibility
- 웹 접근성
- 디지털 접근성

### test_collection.py

**기능:**
- API 키 없이 뉴스 수집 기능만 테스트
- 설정 문제 진단

## 📝 생성되는 콘텐츠 규칙

Gemini API에 전달되는 프롬프트는 다음을 보장합니다:

1. ✅ **요약(Summary) 섹션** 최상단 배치
2. ✅ **구조화된 본문** (대제목, 소제목)
3. ✅ **출처 명시** (모든 정보에 URL 링크)
4. ✅ **결론(Conclusion) 섹션** 실무 전략 포함

## 🎯 커스터마이징

### 검색 키워드 변경

`collect_news.py`:

```python
SEARCH_KEYWORDS = [
    "web accessibility WCAG",
    # 여기에 원하는 키워드 추가
]
```

### 수집 개수 조정

`collect_news.py`의 `collect_all_news()`:

```python
articles = fetch_google_news(keyword, num_results=5)  # 5 -> 원하는 개수
```

### AI 모델 변경

`collect_news.py`의 `generate_markdown_with_gemini()`:

```python
model = genai.GenerativeModel('gemini-2.0-flash-exp')  # 다른 모델로 변경
```

## 🔄 자동화

### Cron (Linux/macOS)

매일 오전 9시 실행:

```bash
crontab -e
```

추가:
```
0 9 * * * cd /path/to/kakao-a11y-news && python3 scripts/collect_news.py
```

### Windows Task Scheduler

1. 작업 스케줄러 열기
2. 기본 작업 만들기
3. 프로그램: `python`
4. 인수: `scripts/collect_news.py`
5. 시작 위치: 프로젝트 경로

## 🐛 문제 해결

### ImportError: No module named 'google.generativeai'

```bash
pip install -r requirements.txt
```

### "GEMINI_API_KEY가 설정되지 않았습니다"

1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. API 키가 올바른지 확인

### 뉴스가 수집되지 않음

1. 인터넷 연결 확인
2. `test_collection.py`로 기본 기능 테스트
3. 다른 키워드 시도

## 📚 더 알아보기

자세한 내용은 프로젝트 루트의 `AUTOMATION_GUIDE.md`를 참고하세요.
