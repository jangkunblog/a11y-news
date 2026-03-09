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
from datetime import datetime, timedelta
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

# reference/a11y-weekly/reference/sources.md 기반 5개 카테고리별 검색 키워드
# 카테고리별 최소 1개·최대 5개 항목, 지난 1주 이내 콘텐츠 우선
CATEGORY_KEYWORDS = {
    "국내외 뉴스": [
        "web accessibility news",
        "디지털 접근성",
        "웹 접근성 뉴스",
        "카카오 접근성",
    ],
    "표준 업데이트": [
        "WCAG update",
        "WAI-ARIA update",
        "W3C accessibility",
    ],
    "도구 & 기술": [
        "accessibility tool release",
        "axe-core update",
        "screen reader update",
        "접근성 검사 도구",
    ],
    "법률 & 정책": [
        "accessibility law",
        "EU accessibility act",
        "장애인차별금지법",
        "정보통신 접근성",
    ],
    "실무 사례 & 가이드": [
        "accessibility best practice",
        "a11y guide",
        "접근성 개선 사례",
    ],
}

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
            content = extract_text_from_url(url)
            source = url.split("/")[2] if "//" in url else "Web"
            # 본문이 충분하면 본문 사용, 아니어도 URL은 수집해 두어 0건 방지(많은 사이트가 봇/JS로 본문 차단)
            if content and len(content) > 100:
                results.append({
                    "title": f"웹 문서",
                    "link": url,
                    "summary": content,
                    "source": source,
                })
            else:
                # 본문 추출 실패 시에도 링크만으로 항목 추가 → Gemini가 링크 기준으로 다이제스트 작성 가능
                results.append({
                    "title": f"웹 문서 ({source})",
                    "link": url,
                    "summary": f"[본문 자동 추출 실패. 검색 쿼리: {query}. 해당 URL을 출처로만 참고하세요.]",
                    "source": source,
                })
            time.sleep(1)
        print(f"   ✓ {len(results)}개 페이지 수집 (본문 추출 성공 + 링크만 포함)")
        return results
        
    except Exception as e:
        print(f"   ✗ 검색/크롤링 오류 발생: {str(e)}")
        return []

def collect_data(keywords: List[str], max_per_keyword: int = 5) -> List[Dict]:
    """단일 키워드 목록으로 수집 (심층 분석 모드용)."""
    all_data = []
    for keyword in keywords:
        articles = fetch_search_and_scrape(keyword, num_results=max_per_keyword)
        all_data.extend(articles)
    seen_links = set()
    unique_data = []
    for item in all_data:
        if item["link"] not in seen_links:
            seen_links.add(item["link"])
            unique_data.append(item)
    print(f"\n✓ 총 {len(unique_data)}개의 웹 문서 본문 크롤링 완료\n")
    return unique_data


def collect_data_by_categories(max_per_keyword: int = 3) -> List[Dict]:
    """reference 5개 카테고리별로 검색해 수집. 각 항목에 category 키를 부여."""
    all_data = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        print(f"\n📂 카테고리: {category}")
        for keyword in keywords[:2]:  # 카테고리당 최대 2개 키워드로 제한
            articles = fetch_search_and_scrape(keyword, num_results=max_per_keyword)
            for a in articles:
                a["category"] = category
                all_data.append(a)
            time.sleep(0.5)
    seen_links = set()
    unique_data = []
    for item in all_data:
        if item["link"] not in seen_links:
            seen_links.add(item["link"])
            unique_data.append(item)
    print(f"\n✓ 총 {len(unique_data)}개 항목 수집 (카테고리별)\n")
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

    # reference: templates/weekly-digest-template.md + reference/sources.md 수집 규칙
    week_end = datetime.now()
    week_start = week_end - timedelta(days=6)
    date_range = f"{week_start.strftime('%Y.%m.%d')} ~ {week_end.strftime('%m.%d')}"

    weekly_prompt = f"""
역할: 너는 웹 접근성(A11Y)과 디지털 포용 주간 다이제스트 전문 큐레이터야.
아래 <수집된 웹 페이지 본문 자료>는 카테고리별로 수집한 것이야. 이 자료만 바탕으로 'A11Y 주간 다이제스트' 포스트를 작성해.

<수집된 웹 페이지 본문 자료>
{data_json}
</수집된 웹 페이지 본문 자료>

[필수 문서 구조 — 반드시 이 순서와 형식을 따를 것]

1. **도입부** (섹션 제목 없이 본문 맨 위에 1~2문단)
   - 이번 주 접근성 소식 요약. 가장 주목할 만한 뉴스를 하이라이트하고 전체 흐름을 간략히 소개.

2. **## 국내외 뉴스**
   - 각 항목: ### [뉴스 제목] → 2~3줄 요약(왜 중요한지, 어떤 영향인지) → 다음 줄에 출처 블록.
   - 출처 형식: > 출처: [출처명](URL) (YYYY.MM.DD)
   - 해당 카테고리 자료가 없으면 "이번 주에는 주요 업데이트가 없었습니다." 한 줄만 적기.

3. **## 표준 업데이트 (WCAG, WAI-ARIA 등)**
   - 같은 형식: ### 제목, 2~3줄 요약, > 출처: [출처명](URL) (YYYY.MM.DD)
   - 없으면 "이번 주에는 주요 업데이트가 없었습니다."

4. **## 도구 & 기술**
   - 동일 형식. 없으면 "이번 주에는 주요 업데이트가 없었습니다."

5. **## 법률 & 정책**
   - 동일 형식. 없으면 "이번 주에는 주요 업데이트가 없었습니다."

6. **## 실무 사례 & 가이드**
   - 동일 형식. 없으면 "이번 주에는 주요 업데이트가 없었습니다."

7. **## 마무리**
   - 1~2문단: 이번 주 핵심 요약, 주목할 변화, 다음 주 예고. 독자에게 접근성 실천을 독려하는 메시지로 마무리.

[작성 규칙]
- 환각 금지: 제공된 자료에 있는 사실과 링크만 사용. 자료에 없는 URL이나 제목을 만들지 마라.
- 카테고리(category) 필드가 있는 항목은 해당 카테고리 섹션에만 배치해.
- 각 섹션당 최소 1개 최대 5개 항목. 항목이 없으면 "이번 주에는 주요 업데이트가 없었습니다." 로만 표기.
- 날짜는 자료에 없으면 이번 주 범위({date_range}) 중 하루로 추정해 YYYY.MM.DD 형식으로 출처에 기재.
- 이모지 사용 금지.
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

def create_blog_post(content: str, title_prefix: str, is_weekly_digest: bool = False) -> str:
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    time_str = today.strftime('%H%M%S')
    filename = f"a11y-news-{date_str}-{time_str}.md"
    pub_date_iso = today.strftime("%Y-%m-%dT%H:%M:%S")
    # reference: title/description 스타일
    if is_weekly_digest:
        title = title_prefix
        description = f"{title_prefix} 웹 접근성과 디지털 포용 관련 주간 뉴스 다이제스트"
    else:
        title = f"{title_prefix} - {today.strftime('%Y년 %m월 %d일')}"
        description = "최신 웹 접근성 및 디지털 포용성 분석 리포트"
    frontmatter = f"""---
title: '{title}'
description: '{description}'
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
            print("📰 [주간 다이제스트 모드] 실행 중...")
            data = collect_data_by_categories(max_per_keyword=3)
            # reference: "A11Y 주간 다이제스트: YYYY.MM.DD ~ MM.DD"
            week_end = datetime.now()
            week_start = week_end - timedelta(days=6)
            title_prefix = f"A11Y 주간 다이제스트: {week_start.strftime('%Y.%m.%d')} ~ {week_end.strftime('%m.%d')}"
            
        if not data:
            print("⚠️ 수집된 웹 데이터가 없습니다.")
            return
            
        markdown_content = generate_markdown_with_gemini(data, is_deep_dive, args.custom_prompt)
        file_path = create_blog_post(markdown_content, title_prefix, is_weekly_digest=not is_deep_dive)
        
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