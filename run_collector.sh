#!/bin/bash
# 뉴스 수집 스크립트 실행 헬퍼

echo "🌐 디지털 접근성 뉴스 수집기"
echo "================================"
echo ""

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3이 설치되어 있지 않습니다."
    echo "   Python 3.8 이상을 설치해주세요."
    exit 1
fi

echo "✓ Python 버전: $(python3 --version)"
echo ""

# .env 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다."
    echo ""
    echo "다음 단계를 진행하세요:"
    echo "1. cp .env.example .env"
    echo "2. .env 파일을 열어 GEMINI_API_KEY 입력"
    echo "3. 다시 이 스크립트 실행"
    echo ""
    exit 1
fi

# 의존성 확인
echo "📦 의존성 확인 중..."
python3 -c "import google.generativeai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  필요한 패키지가 설치되지 않았습니다."
    echo ""
    read -p "지금 설치하시겠습니까? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install -r requirements.txt
    else
        echo "❌ 설치가 취소되었습니다."
        exit 1
    fi
fi

echo "✓ 의존성 확인 완료"
echo ""

# 스크립트 실행
echo "🚀 뉴스 수집 시작..."
echo ""
python3 scripts/collect_news.py

echo ""
echo "✅ 완료!"
