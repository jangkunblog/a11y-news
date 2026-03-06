#!/usr/bin/env python3
"""
디지털 접근성 웹 데이터 수집 및 마크다운 리포트 생성 스크립트 (최신 SDK 적용)
"""

import os
import sys
import json
import argparse
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# 새로운 Gemini SDK 적용
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("⚠️ 'google-genai' 라이브러리가 설치되지 않았습니다.")
    sys.exit(1)

# googlesearch-python (무료, API 키 불필요)
try:
    from googlesearch import search as google_search
except ImportError:
    print("⚠️ 'googlesearch-python' 라이브러리가 설치되지 않았습니다. pip install googlesearch-python")
    sys.exit(1)

# 환경 변수 로드
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BLOG_CONTENT_PATH = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

if not GEMINI_API_KEY:
    print("⚠️ 경고: GEMINI_API_KEY가 설정되지 않았습니다.")
    sys.exit(1)

# Gemini 클라이언트 초기화 (새로운 방식)
client = genai.Client(api_key=GEMINI_API_KEY)

DEFAULT_WEEKLY_KEYWORDS = [
    "W3C web accessibility updates",
    "웹 접근성 동향",
    "디지털 접근성 가이드라인",
    "장애인차별금지법 IT",
    "screen reader AI updates"
]

def fetch_web_data(query: str, num_results: int = 10) -> List[Dict]:
    """googlesearch-python으로 Google 웹 검색 (무료, API 키 불필요)"""
    print(f"🔍 웹 검색 중: '{query}'")
    results = []
    num_results = min(num_results, 20)  # 요청당 적당한 수
    try:
        # advanced=True → title, url, description 반환
        search_results = google_search(
            query,
            num_results=num_results,
            advanced=True,
            lang="ko",
            sleep_interval=2,  # 요청 간격 (차단 방지)
        )
        for r in search_results:
            link = getattr(r, "url", "") or ""
            results.append({
                "title": getattr(r, "title", "") or "",
                "link": link,
                "summary": getattr(r, "description", "") or "",
                "source": urllib.parse.urlparse(link).netloc if link else "Web",
            })
        print(f"   ✓ {len(results)}개 웹 문서 발견")
        time.sleep(1)
        return results
    except Exception as e:
        print(f"   ✗ 검색 오류 발생: {str(e)}")
        return []

def collect_data(keywords: List[str], max_per_keyword: int) -> List[Dict]:
    all_data = []
    for keyword in keywords:
        articles = fetch_web_data(keyword, num_results=max_per_keyword)
        all_data.extend(articles)
    
    seen_links = set()
    unique_data = []
    for item in all_data:
        if item['link'] not in seen_links:
            seen_links.add(item['link'])
            unique_data.append(item)
            
    print(f"\n✓ 총 {len(unique_data)}개의 고유 웹 문서 수집 완료\n")
    return unique_data

def generate_markdown_with_gemini(data: List[Dict], is_deep_dive: bool, custom_prompt: str = None) -> str:
    print("🤖 Gemini API로 전문 리포트 작성 중...\n")
    
    data_json = json.dumps(data, ensure_ascii=False, indent=2)
    
# 기존 코드의 deep_dive_prompt와 weekly_prompt 부분을 아래 내용으로 덮어써주세요.

    deep_dive_prompt = f"""
역할: 너는 디지털 접근성, 배리어프리(Barrier-free), 디지털 포용성(Digital Inclusion) 및 ESG 경영 전문가야.
제공된 <수집된 웹 자료>를 바탕으로 사용자가 요청한 주제에 대한 '심층 분석 리포트'를 작성해.

<수집된 웹 자료>
{data_json}
</수집된 웹 자료>

<사용자 요청 사항>
{custom_prompt if custom_prompt else "제공된 자료를 바탕으로 해당 주제에 대해 심도 있게 분석해줘."}
</사용자 요청 사항>

[작성 규칙]
1. 넓은 의미의 접근성 포함: WCAG, ARIA 같은 기술적 표준뿐만 아니라, 장애인/고령자/소외계층을 위한 UI/UX 개선, 서비스 기획, 배리어프리 활동, 디지털 포용성 정책, 관련 ESG 활동을 모두 '디지털 접근성'의 범주로 인정하고 적극적으로 본문에 포함해.
2. 환각 금지: 반드시 제공된 <수집된 웹 자료>의 사실에만 기반하여 작성하되, 제공된 정보가 적더라도 있는 정보를 최대한 자세히 풀어서 유기적인 글로 작성해.
3. 문서 구조:
   - ## Summary: 핵심 내용 3~4줄 요약. (이모지 금지)
   - ## 심층 분석 (대제목): 논리적 흐름에 따라 소제목(###)을 나누어 깊이 있게 작성.
   - ⚠️ 각 주장이나 정보 뒤에는 반드시 출처를 인용해. 형식: `([출처: 매체명/제목](URL))`
4. ## 결론 (Conclusion): 맨 마지막에 포함. 분석을 바탕으로 실무자가 참고할 점, 향후 전략적 방향성을 제시해.
"""

    weekly_prompt = f"""
역할: 너는 디지털 접근성, 배리어프리, 포용적 디자인 전문 정보 큐레이터야.
제공된 <수집된 웹 자료>를 바탕으로 '주간 디지털 접근성 동향 리포트'를 작성해.

<수집된 웹 자료>
{data_json}
</수집된 웹 자료>

[작성 규칙]
1. 넓은 의미의 접근성 포함: 기술적 표준(WCAG)뿐만 아니라, 기업의 배리어프리 캠페인, 장애인 사용자 경험(UX) 개선, 디지털 소외계층 지원 등 '디지털 포용'과 관련된 모든 유의미한 정보를 포함해.
2. 주제별 그룹화: 비슷한 주제끼리 묶어서 소제목(###)으로 구성해.
3. 환각 금지: 제공된 자료의 사실에만 기반해.
4. 문서 구조:
   - ## Summary: 핵심 트렌드 3~4줄 요약. (이모지 금지)
   - ## 주간 동향 분석 (대제목): 그룹화된 주제별 서술. 정보 뒤에 반드시 출처 인용. 형식: `([출처: 매체명/제목](URL))`
5. ## 결론 및 전략 (Conclusion): 맨 마지막에 포함. 향후 대응 전략 3가지 이상을 전략적으로 제시해.
"""

    final_prompt = deep_dive_prompt if is_deep_dive else weekly_prompt

    max_retries = 3
    base_delay = 10  # 초

    for attempt in range(max_retries):
        try:
            # 새로운 google-genai 문법 적용
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
            err_str = str(e)
            is_503 = '503' in err_str or 'UNAVAILABLE' in err_str or 'high demand' in err_str.lower()
            if is_503 and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"⚠️ Gemini API 일시 과부하(503). {delay}초 후 재시도 ({attempt + 1}/{max_retries})...")
                time.sleep(delay)
            else:
                print(f"✗ Gemini API 오류: {err_str}")
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
    parser = argparse.ArgumentParser(description='디지털 접근성 웹 데이터 수집 및 리포트 생성기')
    parser.add_argument('--keywords', nargs='+', help='특정 주제 심층 분석용 키워드')
    parser.add_argument('--custom-prompt', type=str, help='Gemini에 전달할 추가 지시사항')
    
    args = parser.parse_args()
    
    is_deep_dive = bool(args.keywords or args.custom_prompt)
    
    print("\n" + "🌐 " * 20)
    print("   디지털 접근성 리포트 자동 생성기")
    print("🌐 " * 20 + "\n")
    
    try:
        if is_deep_dive:
            print("🚀 [심층 분석 모드] 실행 중...")
            search_keywords = args.keywords if args.keywords else ["디지털 접근성"]
            data = collect_data(search_keywords, max_per_keyword=15)
            title_prefix = f"심층 분석: {', '.join(search_keywords)}"
        else:
            print("📰 [주간 동향 모드] 실행 중...")
            data = collect_data(DEFAULT_WEEKLY_KEYWORDS, max_per_keyword=5)
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
        print(f"📊 수집/분석된 웹 문서: {len(data)}개")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()