#!/usr/bin/env python3
"""
뉴스 수집 스크립트 테스트
API 키 없이 기본 뉴스 수집 기능만 테스트합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.collect_news import fetch_google_news, SEARCH_KEYWORDS


def main():
    print("\n" + "="*60)
    print("🧪 뉴스 수집 기능 테스트")
    print("="*60 + "\n")
    
    print("이 테스트는 Gemini API 키 없이 실행됩니다.")
    print("뉴스 수집 기능만 확인합니다.\n")
    
    total_articles = 0
    
    for keyword in SEARCH_KEYWORDS[:2]:  # 처음 2개만 테스트
        articles = fetch_google_news(keyword, num_results=3)
        total_articles += len(articles)
        
        if articles:
            print(f"\n   샘플 뉴스:")
            for i, article in enumerate(articles[:2], 1):
                print(f"   {i}. {article['title'][:60]}...")
                print(f"      {article['link'][:80]}...")
        
        print()
    
    print("="*60)
    if total_articles > 0:
        print(f"✅ 테스트 성공! 총 {total_articles}개 뉴스 수집됨")
        print("\n💡 다음 단계:")
        print("   1. .env 파일에 GEMINI_API_KEY 설정")
        print("   2. python scripts/collect_news.py 실행")
    else:
        print("⚠️  뉴스를 찾지 못했습니다.")
        print("   인터넷 연결을 확인하세요.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
