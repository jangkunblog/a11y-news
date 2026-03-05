#!/usr/bin/env python3
"""
디지털 접근성 뉴스 수집 및 마크다운 생성 스크립트

이 스크립트는 Google News RSS를 통해 접근성 관련 뉴스를 수집하고,
Gemini API를 사용하여 요약 및 구조화된 마크다운 파일을 생성합니다.
"""

import os
import sys
import json
import argparse
import requests
import feedparser
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from urllib.parse import quote_plus
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

# 기본 뉴스 검색 키워드 (다양한 소스 포함)
DEFAULT_SEARCH_KEYWORDS = [
    # 국제 표준 및 가이드라인
    "WCAG accessibility",
    "W3C accessibility",
    "ARIA accessibility",
    "mobile accessibility",
    "Google accessibility",
    "Apple accessibility",
    
    # 한국어 키워드
    "접근성",
    "웹 접근성",
    "디지털 접근성",
    "장애인 접근성",
    
    # AI 및 신기술
    "AI accessibility",
    "인공지능 접근성",
    "robot accessibility",
    
    # 플랫폼 및 기술
    "screen reader",
    "VoiceOver accessibility",
    "TalkBack accessibility",
    "모바일 접근성",
    
    # 법규 및 정책
    "accessibility compliance",
    "접근성 법규",
    "장애인차별금지법",
    
    # 실무 및 개발
    "accessible design",
    "inclusive design",
    "접근성 개발",
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
    
    # URL 인코딩 (공백 등 특수문자 처리)
    encoded_query = quote_plus(query)
    
    # Google News RSS URL
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
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


def collect_all_news(custom_keywords: List[str] = None) -> List[Dict]:
    """
    모든 키워드에 대해 뉴스 수집
    
    Args:
        custom_keywords: 커스텀 검색 키워드 리스트 (None이면 기본 키워드 사용)
    
    Returns:
        전체 뉴스 아이템 리스트
    """
    print("\n" + "="*60)
    print("📰 디지털 접근성 뉴스 수집 시작")
    print("="*60 + "\n")
    
    # 키워드 선택
    keywords = custom_keywords if custom_keywords else DEFAULT_SEARCH_KEYWORDS
    
    if custom_keywords:
        print(f"🎯 커스텀 키워드 사용: {len(keywords)}개")
    else:
        print(f"🔍 기본 키워드 사용: {len(keywords)}개")
    print()
    
    all_articles = []
    
    for keyword in keywords:
        articles = fetch_google_news(keyword, num_results=8)  # 키워드당 8개로 증가
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


def generate_markdown_with_gemini(articles: List[Dict], custom_prompt: str = None) -> str:
    """
    Gemini API를 사용하여 뉴스를 요약하고 마크다운으로 변환
    
    Args:
        articles: 뉴스 아이템 리스트
        custom_prompt: 추가 커스텀 프롬프트 (옵션)
        
    Returns:
        마크다운 형식의 문자열
    """
    print("🤖 Gemini API로 콘텐츠 생성 중...\n")
    
    # 뉴스 데이터를 JSON 형식으로 준비
    news_data = json.dumps(articles, ensure_ascii=False, indent=2)
    
    # 커스텀 프롬프트 추가
    additional_instruction = ""
    if custom_prompt:
        additional_instruction = f"\n\n<추가 지시사항>\n{custom_prompt}\n</추가 지시사항>\n"
        print(f"📝 커스텀 프롬프트 적용: {custom_prompt[:50]}...\n")
    
    # Gemini에 전달할 프롬프트 (규칙 하드코딩)
    prompt = f"""
역할: 너는 디지털 접근성(Digital Accessibility) 전문 객관적 리서처이자 전략 분석가야.
제공된 뉴스/업데이트 데이터를 바탕으로 블로그 게시물을 작성해줘.

<뉴스 데이터>
{news_data}
</뉴스 데이터>

[작성 규칙]
1. 최상단 섹션: "## Summary" - 전체 뉴스의 핵심만 3~4줄로 요약.
   - ⚠️ 제목에 이모지를 포함하지 말 것. 단순히 "## Summary"만 사용.

2. 본문 섹션: 제공된 사실만을 바탕으로 대제목(##)/소제목(###)을 나누어 작성.
   - ⚠️ 제목에 이모지를 포함하지 말 것. (예: ## 주요 뉴스, ## 국내 동향)
   - ⚠️ 절대 임의로 사실을 지어내거나 추측하지 말 것.
   - ⚠️ 각 뉴스 항목은 개별 단락(paragraph)으로 작성하고, 항목 끝에 출처를 포함.
   - 형식: 각 뉴스 내용을 하나의 단락으로 작성한 후, 같은 단락 내에서 괄호와 함께 출처 링크 추가.
   - 예시:
     ```
     ### 소제목
     
     첫 번째 뉴스 내용입니다. ([출처: 매체명](URL))
     
     두 번째 뉴스 내용입니다. ([출처: 매체명](URL))
     
     세 번째 뉴스 내용입니다. ([출처: 매체명](URL))
     ```
   - 각 뉴스 항목 사이에는 빈 줄을 하나 넣어 명확히 구분할 것.
   - 출처는 반드시 괄호로 감싸서 표기: ([출처: 매체명](URL))
   - code 사용할 경우에는 내용 영역에 적절히 삽입하세요.
   - 본문 대제목 예시: ## 주요 뉴스, ## 국내 동향, ## 해외 업데이트 등
   - 본문 소제목 예시: ### WCAG 관련, ### 법규/정책, ### 기술/도구 등

3. 최하단 섹션: "## 결론 및 전략" - 이 뉴스들이 IT/기획/개발 실무자들에게 시사하는 바, 앞으로 준비해야 할 접근성 대응 전략 등을 너의 분석력으로 도출해서 작성.
   - ⚠️ 제목에 이모지를 포함하지 말 것. 단순히 "## 결론 및 전략"만 사용.
   - 실무자 관점에서 핵심 포인트 정리
   - 향후 대응 전략 및 실행 방안
   - 주의해야 할 사항이나 변화의 의미
{additional_instruction}
<출력 형식>
- 마크다운 본문만 출력하세요.
- 프론트매터(---)는 제외하고 본문만 작성하세요.
- 모든 내용은 한국어를 기반으로 작성하세요.
- 제목(##, ###)에는 절대 이모지를 사용하지 마세요.
- 각 뉴스 항목은 독립된 단락으로 작성하고, 항목 사이에 빈 줄을 넣으세요.
- 뉴스 내용과 출처는 같은 단락 안에 함께 작성하세요.
- 출처 형식: 반드시 괄호로 감싸서 "([출처: 매체명](URL))" 형태로 작성하세요.
- 출처 URL은 절대 생략하지 말고 반드시 포함하세요.
</출력 형식>
"""
    
    try:
        # Gemini 모델 설정 (2025년 최신 안정 모델 - 2.5 Flash)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
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
    # 현재 날짜와 시간으로 파일명 생성 (동일 날짜 여러 게시물 지원)
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    time_str = today.strftime('%H%M%S')
    filename = f"a11y-news-{date_str}-{time_str}.md"
    
    # 프론트매터 생성 (pubDate에 시간 포함하여 정렬)
    pub_date_full = today.strftime("%b %d %Y %H:%M:%S")
    frontmatter = f"""---
title: '디지털 접근성 뉴스 - {today.strftime("%Y년 %m월 %d일 %H:%M")}'
description: '최신 웹 접근성 및 WCAG 관련 뉴스 모음'
pubDate: '{pub_date_full}'
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
    # 커맨드라인 인자 파싱
    parser = argparse.ArgumentParser(
        description='디지털 접근성 뉴스를 자동으로 수집하고 블로그 게시물을 생성합니다.'
    )
    parser.add_argument(
        '--keywords',
        nargs='+',
        help='검색할 키워드 (여러 개 가능). 예: --keywords "WCAG 3.0" "ARIA updates"'
    )
    parser.add_argument(
        '--custom-prompt',
        type=str,
        help='Gemini에 추가로 전달할 커스텀 프롬프트'
    )
    
    args = parser.parse_args()
    
    print("\n" + "🌐 " * 20)
    print("   디지털 접근성 뉴스 자동 수집기")
    print("🌐 " * 20 + "\n")
    
    try:
        # 1. 뉴스 수집
        custom_keywords = args.keywords if args.keywords else None
        articles = collect_all_news(custom_keywords)
        
        if not articles:
            print("⚠️  수집된 뉴스가 없습니다.")
            return
        
        # 2. Gemini로 콘텐츠 생성
        markdown_content = generate_markdown_with_gemini(articles, args.custom_prompt)
        
        # 3. 마크다운 파일 생성
        file_path = create_blog_post(markdown_content)
        
        # 4. 결과 출력
        print("="*60)
        print("✅ 블로그 게시물 생성 완료!")
        print("="*60)
        print(f"📄 파일 위치: {file_path}")
        print(f"📊 수집된 뉴스: {len(articles)}개")
        if args.keywords:
            print(f"🎯 커스텀 키워드: {', '.join(args.keywords)}")
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
