# 🚀 빠른 시작 가이드

디지털 접근성 뉴스 자동 수집 기능을 5분 안에 설정하세요!

## ⚡ 3단계로 시작하기

### 1️⃣ Gemini API 키 발급 (2분)

1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정으로 로그인
3. **"Create API Key"** 클릭
4. 생성된 API 키 복사 📋

> 💡 **무료 티어**: 월 60회 무료 요청 가능

### 2️⃣ 환경 설정 (2분)

```bash
# 1. .env 파일 생성
cp .env.example .env

# 2. .env 파일 열기
# macOS: open .env
# Windows: notepad .env
# Linux: nano .env

# 3. API 키 붙여넣기
# GEMINI_API_KEY=여기에_복사한_API_키_붙여넣기

# 4. Python 패키지 설치
pip install -r requirements.txt
```

### 3️⃣ 실행! (1분)

```bash
# 방법 1: 간편 실행 (macOS/Linux)
./run_collector.sh

# 방법 2: 직접 실행
python scripts/collect_news.py
```

## ✅ 성공 확인

스크립트가 성공적으로 실행되면:

1. ✅ 콘솔에 "블로그 게시물 생성 완료!" 메시지 표시
2. ✅ `src/content/blog/a11y-news-YYYY-MM-DD.md` 파일 생성
3. ✅ Astro 개발 서버가 실행 중이면 자동 반영

브라우저에서 http://localhost:4322/blog 를 새로고침하여 확인하세요!

## 🧪 테스트만 해보기 (API 키 불필요)

```bash
python scripts/test_collection.py
```

뉴스 수집 기능만 테스트합니다. API 키 없이 실행 가능!

## 📅 정기 실행 설정

### macOS/Linux - Cron

```bash
# cron 편집기 열기
crontab -e

# 매주 월요일 오전 9시 실행 (아래 라인 추가)
0 9 * * 1 cd /path/to/kakao-a11y-news && /usr/bin/python3 scripts/collect_news.py
```

### Windows - 작업 스케줄러

1. **작업 스케줄러** 실행
2. **기본 작업 만들기** 선택
3. 설정:
   - 이름: "접근성 뉴스 수집"
   - 트리거: 매주 월요일 오전 9시
   - 프로그램: `python`
   - 인수: `scripts/collect_news.py`
   - 시작 위치: `프로젝트_경로`

## 🎯 실행 예시

```bash
$ python scripts/collect_news.py

🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 
   디지털 접근성 뉴스 자동 수집기
🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 🌐 

============================================================
📰 디지털 접근성 뉴스 수집 시작
============================================================

🔍 검색 중: 'web accessibility WCAG'
   ✓ 5개 뉴스 발견
🔍 검색 중: 'digital accessibility standards'
   ✓ 5개 뉴스 발견
🔍 검색 중: 'ARIA accessibility'
   ✓ 4개 뉴스 발견
🔍 검색 중: '웹 접근성'
   ✓ 5개 뉴스 발견
🔍 검색 중: '디지털 접근성'
   ✓ 6개 뉴스 발견

✓ 총 18개의 고유 뉴스 수집 완료

🤖 Gemini API로 콘텐츠 생성 중...

✓ 콘텐츠 생성 완료

============================================================
✅ 블로그 게시물 생성 완료!
============================================================
📄 파일 위치: src/content/blog/a11y-news-2026-03-05.md
📊 수집된 뉴스: 18개
📅 생성 일시: 2026-03-05 15:30:42

💡 Astro 개발 서버에서 자동으로 반영됩니다.
   브라우저를 새로고침하여 확인하세요!
```

## 🔧 문제 해결

### "GEMINI_API_KEY가 설정되지 않았습니다"
➡️ `.env` 파일에 API 키 입력 확인

### "No module named 'google'"
➡️ `pip install -r requirements.txt` 실행

### "수집된 뉴스가 없습니다"
➡️ 인터넷 연결 확인 또는 다른 시간에 재시도

### API 할당량 초과
➡️ 24시간 후 재시도 또는 유료 플랜 고려

## 📚 더 알아보기

- 📖 [전체 가이드](./AUTOMATION_GUIDE.md) - 상세한 설명 및 고급 설정
- 🔧 [스크립트 문서](./scripts/README.md) - 커스터마이징 방법
- 🤖 [Gemini API](https://ai.google.dev/docs) - API 문서

## 💬 도움이 필요하신가요?

- 이슈가 있다면 GitHub Issues에 등록해주세요
- 개선 아이디어는 Pull Request로 기여해주세요!

---

**즐거운 접근성 뉴스 아카이빙 되세요! 🎉**
