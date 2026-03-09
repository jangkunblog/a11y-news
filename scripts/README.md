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
- 구글 검색(googlesearch-python) + 선택적 본문 크롤링(BeautifulSoup)으로 접근성 뉴스 수집
- Gemini API로 주간 다이제스트 또는 심층 분석 리포트 생성
- 마크다운 블로그 게시물 자동 생성

**실행 모드:**
- **기본(주간 다이제스트)**: `python scripts/collect_news.py` — 5개 카테고리별 검색 후 다이제스트 형식으로 작성
- **심층 분석**: `python scripts/collect_news.py --keywords "WCAG 3.0" "ARIA"` 또는 `--custom-prompt "..."`

**필수 환경 변수:**
- `GEMINI_API_KEY`: Google Gemini API 키

**생성 파일:**
- `src/content/blog/a11y-news-YYYY-MM-DD-HHMMSS.md`

**주간 다이제스트 카테고리·키워드** (`reference/a11y-weekly/reference/sources.md` 기반):
- 국내외 뉴스, 표준 업데이트, 도구 & 기술, 법률 & 정책, 실무 사례 & 가이드
- 카테고리별 키워드는 `collect_news.py`의 `CATEGORY_KEYWORDS` 참고

### test_collection.py

**기능:**
- API 키 없이 뉴스 수집 기능만 테스트
- 설정 문제 진단

## 📝 생성되는 콘텐츠 규칙

**주간 다이제스트 모드** (`reference` 템플릿 기반):
1. **도입부** — 이번 주 소식 1~2문단 요약
2. **## 국내외 뉴스** · **## 표준 업데이트** · **## 도구 & 기술** · **## 법률 & 정책** · **## 실무 사례 & 가이드** — 항목별 `### 제목`, 2~3줄 요약, `> 출처: [출처명](URL) (YYYY.MM.DD)`
3. **## 마무리** — 핵심 요약 및 독자 독려 메시지

**심층 분석 모드:** Summary → 심층 분석(소제목) → 결론(Conclusion), 출처 인용 포함.

## 🎯 커스터마이징

### 주간 다이제스트 키워드 변경

`collect_news.py`의 `CATEGORY_KEYWORDS`에서 카테고리별 검색어를 수정합니다.

### 수집 개수 조정

`collect_news.py`에서 `collect_data_by_categories(max_per_keyword=3)` 또는 `collect_data(..., max_per_keyword=5)`의 인자를 변경합니다.

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
0 9 * * * cd /path/to/a11y-news && python3 scripts/collect_news.py
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
