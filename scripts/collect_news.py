#!/usr/bin/env python3
"""
디지털 접근성 웹 검색 및 '본문 크롤링' 기반 심층 리포트 생성 스크립트
"""

import os
import sys
import json
import argparse
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# 웹 검색 라이브러리
try:
    from googlesearch import search
except ImportError:
    print("⚠️ 'googlesearch-python' 라이브러리가 설치되지 않았습니다.")
    sys.exit(1)

# 새로운 Gemini SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("⚠️ 'google-genai' 라이브러리가 설치되지 않았습니다.")
    sys.exit(1)

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BLOG_CONTENT_PATH = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

if not GEMINI_API_KEY:
    print("⚠️ 경고: GEMINI_API_KEY가 설정되지 않았습니다.")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

DEFAULT_WEEKLY_KEYWORDS = [
    "웹 접근성 동향",
    "디지털 포용성 ESG",
    "배리어프리 IT 카카오 네이버",
    "무장애 점자 스마트",
]

def extract_text_from_url(url: str) -> str:
    """URL에 직접 접속하여 웹페이지 본문(텍스트)을 크롤링합니다."""
    try:
        # 봇 차단을 막기 위한 User-Agent 설정
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=7)
        response.raise_for_status()
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 불필요한 태그(메뉴, 스크립트, 광고 등) 제거
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()
            
        # 주로 본문이 담기는 <p> 태그의 텍스트만 추출
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # 내용이 없으면 div 태그라도 긁어오기
        if len(text) < 100:
            text = soup.get_text(separator=' ', strip=True)
            
        # 너무 긴 문서는 Gemini 토큰 한도를 위해 앞부분 2000자만 자름 (가장 핵심 내용)
        return text[:2000] if len(text) > 2000 else text
        
    except Exception as e:
        print(f"      - ⚠️ 본문 추출 실패 ({url[:40]}...): {str(e)}")
        return ""

def fetch_search_and_scrape(query: str, num_results: int = 5) -> List[Dict]:
    """구글 검색 후 각각의 URL에서 본문을 추출합니다."""
    print(f"\n🔍 구글 검색 및 본문 크롤링 중: '{query}'")
    results = []
    
    try:
        # advanced=True 지원 버전일 경우 dict로 받음, 아니면 url string 제너레이터
        urls = search(query, num_results=num_results, lang="ko")
        
        for url in urls:
            print(f"   -> 페이지 분석 중: {url[:60]}...")
            
            # 여기서 핵심! 검색된 URL의 본문 내용을 직접 긁어옵니다.
            content = extract_text_from_url(url)
            
            # 본문이 유의미하게 추출된 경우에만 데이터에 포함
            if content and len(content) > 100:
                results.append({
                    'title': f"웹 문서",
                    'link': url,
                    'summary': content, # 단순 요약이 아닌 실제 본문 텍스트가 들어감!
                    'source': url.split('/')[2] if '//' in url else 'Web'
                })
            time.sleep(1) # 서버에 무리가 가지 않도록 1초 대기
            
        print(f"   ✓ {len(results)}개 페이지 본문 성공적 추출")
        return results
        
    except Exception as e:
        print(f"   ✗ 검색/크롤링 오류 발생: {str(e)}")
        return []

def collect_data(keywords: List[str], max_per_keyword: int = 5) -> List[Dict]:
    all_data = []
    for keyword in keywords:
        articles = fetch_search_and_scrape(keyword, num_results=max_per_keyword)
        all_data.extend(articles)
    
    seen_links = set()
    unique_data = []
    for item in all_data:
        if item['link'] not in seen_links:
            seen_links.add(item['link'])
            unique_data.append(item)
            
    print(f"\n✓ 총 {len(unique_data)}개의 웹 문서 본문 크롤링 완료\n")
    return unique_data

def generate_markdown_with_gemini(data: List[Dict], is_deep_dive: bool, custom_prompt: str = None) -> str:
    print("🤖 Gemini API로 전문 리포트 작성 중...\n")
    
    data_json = json.dumps(data, ensure_ascii=False, indent=2)
    
    deep_dive_prompt = f"""
역할: 너는 디지털 접근성, 배리어프리, ESG 경영 전문가야.
아래 <수집된 웹 페이지 본문 자료>는 내가 파이썬으로 직접 웹사이트를 돌아다니며 긁어온 실제 본문 텍스트들이야.
이 풍부한 내용을 바탕으로 사용자가 요청한 주제에 대한 '심층 분석 리포트'를 작성해.

<수집된 웹 페이지 본문 자료>
{data_json}
</수집된 웹 페이지 본문 자료>

<사용자 요청 사항>
{custom_prompt if custom_prompt else "제공된 자료를 바탕으로 해당 주제에 대해 심도 있게 분석해줘."}
</사용자 요청 사항>

[작성 규칙]
1. 구체적 사실 인용: 제공된 자료에 있는 카카오, 네이버, 지자체 등의 구체적인 사업 이름(예: 점자달력, 무장애나눔길, 배리어프리 키오스크 등)과 수치를 적극적으로 본문에 녹여내. 내용이 풍부하므로 아주 자세하게 작성해.
2. 환각 금지: 반드시 제공된 자료에 있는 사실에만 기반해 작성해.
3. 문서 구조:
   - ## Summary: 핵심 내용 3~4줄 요약. (이모지 금지)
   - ## 심층 분석 (대제목): 논리적 흐름에 따라 소제목(###)을 나누어 깊이 있게 작성.
   - 각 주장이나 정보 뒤에는 반드시 출처를 인용해. 형식: `([출처: 매체명/제목](URL))`
4. ## 결론 (Conclusion): 맨 마지막에 포함. 분석을 바탕으로 실무자가 참고할 점, 향후 전략적 방향성을 제시해.
"""

    weekly_prompt = f"""
역할: 너는 디지털 접근성 전문 정보 큐레이터야.
아래 <수집된 웹 페이지 본문 자료>를 바탕으로 '주간 디지털 접근성 동향 리포트'를 상세하게 작성해.

<수집된 웹 페이지 본문 자료>
{data_json}
</수집된 웹 페이지 본문 자료>

[작성 규칙]
1. 상세한 내용 작성: 기업/지자체의 구체적인 활동(점자달력, 무장애나눔길 등)과 기술 업데이트를 묶어서 아주 상세하게 작성해.
2. 주제별 그룹화: 비슷한 주제끼리 묶어서 소제목(###)으로 구성해.
3. 문서 구조:
   - ## Summary: 핵심 트렌드 3~4줄 요약. (이모지 금지)
   - ## 주간 동향 분석 (대제목): 그룹화된 주제별 서술. 정보 뒤에 반드시 출처 인용. 형식: `([출처: 매체명/제목](URL))`
4. ## 결론 및 전략 (Conclusion): 맨 마지막에 포함. 향후 대응 전략을 제시해.
"""

    final_prompt = deep_dive_prompt if is_deep_dive else weekly_prompt

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=final_prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=8000,
            )
        )
        return response.text
    except Exception as e:
        print(f"✗ Gemini API 오류: {str(e)}")
        sys.exit(1)

def create_blog_post(content: str, title_prefix: str) -> str:
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    time_str = today.strftime('%H%M%S')
    filename = f"a11y-news-{date_str}-{time_str}.md"
    
    pub_date_iso = today.strftime("%Y-%m-%dT%H:%M:%S")
    
    frontmatter = f"""---
title: '{title_prefix} - {today.strftime("%Y년 %m월 %d일")}'
description: '최신 웹 접근성 및 디지털 포용성 분석 리포트'
pubDate: '{pub_date_iso}'
heroImage: '../../assets/blog-placeholder-1.jpg'
---

"""
    full_content = frontmatter + content
    
    BLOG_CONTENT_PATH.mkdir(parents=True, exist_ok=True)
    file_path = BLOG_CONTENT_PATH / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return str(file_path)

def main():
    parser = argparse.ArgumentParser(description='디지털 접근성 본문 스크래핑 기반 리포트 생성기')
    parser.add_argument('--keywords', nargs='+', help='특정 주제 심층 분석용 키워드')
    parser.add_argument('--custom-prompt', type=str, help='Gemini에 전달할 추가 지시사항')
    
    args = parser.parse_args()
    is_deep_dive = bool(args.keywords or args.custom_prompt)
    
    print("\n" + "🌐 " * 20)
    print("   디지털 접근성 리포트 자동 생성기 (Web Scraping 탑재)")
    print("🌐 " * 20 + "\n")
    
    try:
        if is_deep_dive:
            print("🚀 [심층 분석 모드] 실행 중...")
            search_keywords = args.keywords if args.keywords else ["디지털 접근성"]
            # 검색당 5개씩 가져와서 본문 파싱 (개수 늘리면 너무 오래걸림)
            data = collect_data(search_keywords, max_per_keyword=5)
            title_prefix = f"심층 분석: {', '.join(search_keywords)}"
        else:
            print("📰 [주간 동향 모드] 실행 중...")
            data = collect_data(DEFAULT_WEEKLY_KEYWORDS, max_per_keyword=3)
            title_prefix = "디지털 접근성 주간 동향"
            
        if not data:
            print("⚠️ 수집된 웹 데이터가 없습니다.")
            return
            
        markdown_content = generate_markdown_with_gemini(data, is_deep_dive, args.custom_prompt)
        file_path = create_blog_post(markdown_content, title_prefix)
        
        print("="*60)
        print("✅ 블로그 게시물 생성 완료!")
        print("="*60)
        print(f"📄 파일 위치: {file_path}")
        print(f"📊 수집 및 분석된 실제 웹 페이지: {len(data)}개")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()