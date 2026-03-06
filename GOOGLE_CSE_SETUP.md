# 웹 검색 설정 (googlesearch-python)

뉴스 수집 스크립트는 **googlesearch-python** 라이브러리를 사용해 Google 웹 검색을 수행합니다.

- **무료**: API 키나 검색엔진 설정이 필요 없습니다.
- **설치**: `pip install googlesearch-python` 또는 `pip install -r requirements.txt`
- **동작**: Google 검색 결과를 스크래핑하는 방식으로, 유료 Google Custom Search API를 사용하지 않습니다.

## 로컬 / GitHub Actions

- **로컬**: `requirements.txt`에 포함되어 있으므로 `pip install -r requirements.txt`만 하면 됩니다.
- **GitHub Actions**: 워크플로우에서 동일한 `requirements.txt`로 자동 설치됩니다.

추가로 설정할 환경 변수는 **GEMINI_API_KEY** (리포트 생성용) 뿐입니다.
