#!/usr/bin/env python3
"""
디지털 접근성 뉴스 수집 및 마크다운 생성 스크립트

이 스크립트는 Google News RSS를 통해 접근성 관련 뉴스를 수집하고,
Gemini API를 사용하여 요약 및 구조화된 마크다운 파일을 생성합니다.
"""

import os
import sys
import json
import requests
import feedparser
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 설정
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BLOG_CONTENT_PATH = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

# Gemini API 설정
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  경고: GEMINI_API_KEY가 설정되지 않았습니다.")
    print("   .env 파일에 API 키를 설정해주세요.")
    sys.exit(1)

# 뉴스 검색 키워드
SEARCH_KEYWORDS = [
    "web accessibility WCAG",
    "digital accessibility standards",
    "ARIA accessibility",
    "웹 접근성",
    "디지털 접근성",
]


def fetch_google_news(query: str, num_results: int = 10) -> List[Dict]:
    """
    Google News RSS를 통해 뉴스 검색
    
    Args:
        query: 검색 키워드
        num_results: 결과 개수
        
    Returns:
        뉴스 아이템 리스트
    """
    print(f"🔍 검색 중: '{query}'")
    
    # Google News RSS URL
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    
    try:
        feed = feedparser.parse(rss_url)
        
        articles = []
        for entry in feed.entries[:num_results]:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'summary': entry.get('summary', ''),
                'source': entry.get('source', {}).get('title', 'Unknown')
            })
        
        print(f"   ✓ {len(articles)}개 뉴스 발견")
        return articles
        
    except Exception as e:
        print(f"   ✗ 오류 발생: {str(e)}")
        return []


def collect_all_news() -> List[Dict]:
    """
    모든 키워드에 대해 뉴스 수집
    
    Returns:
        전체 뉴스 아이템 리스트
    """
    print("\n" + "="*60)
    print("📰 디지털 접근성 뉴스 수집 시작")
    print("="*60 + "\n")
    
    all_articles = []
    
    for keyword in SEARCH_KEYWORDS:
        articles = fetch_google_news(keyword, num_results=5)
        all_articles.extend(articles)
    
    # 중복 제거 (URL 기준)
    seen_links = set()
    unique_articles = []
    for article in all_articles:
        if article['link'] not in seen_links:
            seen_links.add(article['link'])
            unique_articles.append(article)
    
    print(f"\n✓ 총 {len(unique_articles)}개의 고유 뉴스 수집 완료\n")
    return unique_articles


def generate_markdown_with_gemini(articles: List[Dict]) -> str:
    """
    Gemini API를 사용하여 뉴스를 요약하고 마크다운으로 변환
    
    Args:
        articles: 뉴스 아이템 리스트
        
    Returns:
        마크다운 형식의 문자열
    """
    print("🤖 Gemini API로 콘텐츠 생성 중...\n")
    
    # 뉴스 데이터를 JSON 형식으로 준비
    news_data = json.dumps(articles, ensure_ascii=False, indent=2)
    
    # Gemini에 전달할 프롬프트 (규칙 하드코딩)
    prompt = f"""
당신은 디지털 접근성 전문가입니다. 다음 뉴스 데이터를 분석하여 블로그 게시물용 마크다운을 작성해주세요.

<뉴스 데이터>
{news_data}
</뉴스 데이터>

<필수 규칙>
1. **반드시 최상단에 "## 요약(Summary)" 섹션**을 만들고 전체 내용을 3-5문장으로 요약하세요.

2. **본문은 대제목(##), 소제목(###)으로 구조화**하세요. 예시:
   - ## 주요 뉴스
   - ### WCAG 관련 업데이트
   - ### 국내 접근성 동향
   
3. **본문 작성 시 절대적으로 지켜야 할 원칙**:
   - 스스로 내용을 판단하거나 왜곡하지 말 것
   - 유추하지 말 것
   - **반드시 각 정보의 출처(URL)를 마크다운 링크로 명시**할 것
   - 예: [기사 제목](URL) 또는 "[출처: 기사명](URL)"

4. **맨 마지막에 "## 결론(Conclusion)" 섹션**을 만들고:
   - 이번 뉴스들을 기반으로 실무자가 알아야 할 핵심 포인트
   - 향후 대응 전략
   - 실무에서 해야 할 일
   을 구체적으로 분석하여 작성하세요.

5. 모든 제목과 내용은 한국어로 작성하세요.

6. 출처 URL은 절대 생략하지 말고 반드시 포함하세요.

<출력 형식>
마크다운 본문만 출력하세요. 프론트매터(---)는 제외하고 본문만 작성하세요.
</출력 형식>
"""
    
    try:
        # Gemini 모델 설정 (최신 모델 사용)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # 콘텐츠 생성
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # 창의성 낮춤 (정확성 우선)
                max_output_tokens=4000,
            )
        )
        
        print("✓ 콘텐츠 생성 완료\n")
        return response.text
        
    except Exception as e:
        print(f"✗ Gemini API 오류: {str(e)}")
        sys.exit(1)


def create_blog_post(content: str) -> str:
    """
    마크다운 파일 생성
    
    Args:
        content: 마크다운 본문 내용
        
    Returns:
        생성된 파일 경로
    """
    # 현재 날짜로 파일명 생성
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    filename = f"a11y-news-{date_str}.md"
    
    # 프론트매터 생성
    frontmatter = f"""---
title: '디지털 접근성 뉴스 - {today.strftime("%Y년 %m월 %d일")}'
description: '최신 웹 접근성 및 WCAG 관련 뉴스 모음'
pubDate: '{today.strftime("%b %d %Y")}'
heroImage: '../../assets/blog-placeholder-1.jpg'
---

"""
    
    # 전체 콘텐츠
    full_content = frontmatter + content
    
    # 파일 저장
    BLOG_CONTENT_PATH.mkdir(parents=True, exist_ok=True)
    file_path = BLOG_CONTENT_PATH / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return str(file_path)


def main():
    """메인 함수"""
    print("\n" + "🌐 " * 20)
    print("   디지털 접근성 뉴스 자동 수집기")
    print("🌐 " * 20 + "\n")
    
    try:
        # 1. 뉴스 수집
        articles = collect_all_news()
        
        if not articles:
            print("⚠️  수집된 뉴스가 없습니다.")
            return
        
        # 2. Gemini로 콘텐츠 생성
        markdown_content = generate_markdown_with_gemini(articles)
        
        # 3. 마크다운 파일 생성
        file_path = create_blog_post(markdown_content)
        
        # 4. 결과 출력
        print("="*60)
        print("✅ 블로그 게시물 생성 완료!")
        print("="*60)
        print(f"📄 파일 위치: {file_path}")
        print(f"📊 수집된 뉴스: {len(articles)}개")
        print(f"📅 생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n💡 Astro 개발 서버에서 자동으로 반영됩니다.")
        print("   브라우저를 새로고침하여 확인하세요!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
