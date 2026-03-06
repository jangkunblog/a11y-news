#!/usr/bin/env python3
"""
디지털 접근성 웹 데이터 수집 및 마크다운 리포트 생성 스크립트 (개편판)

뉴스 기사뿐만 아니라 블로그, 공식 문서, 커뮤니티 글 등 다양한 웹 데이터를 수집하며,
정기 발행(동향 요약)과 수동 실행(특정 주제 심층 분석)을 분리하여 처리합니다.
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

# 웹 검색 라이브러리 (pip install duckduckgo-search 필요)
try:
    from duckduckgo_search import DDGS
except ImportError:
    print("⚠️ 'duckduckgo-search' 라이브러리가 설치되지 않았습니다.")
    print("터미널에서 'pip install duckduckgo-search'를 실행해주세요.")
    sys.exit(1)

# 환경 변수 로드
load_dotenv()

# 설정
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
BLOG_CONTENT_PATH = Path(__file__).parent.parent / 'src' / 'content' / 'blog'

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  경고: GEMINI_API_KEY가 설정되지 않았습니다.")
    sys.exit(1)

# 정기 발행용 기본 키워드 (넓고 얕은 탐색)
DEFAULT_WEEKLY_KEYWORDS = [
    "W3C web accessibility updates",
    "웹 접근성 동향",
    "디지털 접근성 가이드라인",
    "장애인차별금지법 IT",
    "screen reader AI updates"
]

def fetch_web_data(query: str, num_results: int = 10) -> List[Dict]:
    """
    DuckDuckGo를 사용하여 뉴스, 블로그, 문서 등 광범위한 웹 데이터 검색
    """
    print(f"🔍 웹 검색 중: '{query}'")
    results = []
    
    try:
        with DDGS() as ddgs:
            # text 검색으로 기사, 블로그, 포럼, 문서 등을 모두 가져옴
            search_results = ddgs.text(query, max_results=num_results)
            
            for r in search_results:
                results.append({
                    'title': r.get('title', ''),
                    'link': r.get('href', ''),
                    'summary': r.get('body', ''),
                    'source': r.get('href', '').split('/')[2] if 'href' in r else 'Web'
                })
        
        print(f"   ✓ {len(results)}개 웹 문서 발견")
        time.sleep(1) # Rate limit 방지
        return results
        
    except Exception as e:
        print(f"   ✗ 검색 오류 발생: {str(e)}")
        return []

def collect_data(keywords: List[str], max_per_keyword: int) -> List[Dict]:
    """키워드 리스트를 기반으로 데이터를 수집하고 중복을 제거"""
    all_data = []
    for keyword in keywords:
        articles = fetch_web_data(keyword, num_results=max_per_keyword)
        all_data.extend(articles)
    
    # 중복 제거 (URL 기준)
    seen_links = set()
    unique_data = []
    for item in all_data:
        if item['link'] not in seen_links:
            seen_links.add(item['link'])
            unique_data.append(item)
            
    print(f"\n✓ 총 {len(unique_data)}개의 고유 웹 문서 수집 완료\n")
    return unique_data

def generate_markdown_with_gemini(data: List[Dict], is_deep_dive: bool, custom_prompt: str = None) -> str:
    """수집된 데이터를 바탕으로 Gemini API를 호출하여 리포트 생성"""
    print("🤖 Gemini API로 전문 리포트 작성 중...\n")
    
    data_json = json.dumps(data, ensure_ascii=False, indent=2)
    
    # [1] 심층 분석용 프롬프트 (키워드/수동 실행 시)
    deep_dive_prompt = f"""
역할: 너는 디지털 접근성(WCAG, ARIA 등) 최고 수준의 기술 분석가이자 리서처야.
제공된 <수집된 웹 자료>를 바탕으로 사용자가 요청한 특정 주제에 대한 '심층 분석 리포트'를 작성해.

<수집된 웹 자료>
{data_json}
</수집된 웹 자료>

<사용자 요청 사항 (Custom Prompt)>
{custom_prompt if custom_prompt else "제공된 자료를 바탕으로 해당 주제에 대해 심도 있게 분석해줘."}
</사용자 요청 사항>

[작성 규칙]
1. 자료 나열 금지: 개별 자료를 단순히 나열하지 마. 제공된 여러 출처의 정보를 종합(Synthesis)하여 하나의 유기적이고 전문적인 글로 작성할 것.
2. 환각 금지: 반드시 제공된 <수집된 웹 자료>의 사실에만 기반하여 본문을 작성해. 스스로 지어내지 마.
3. 문서 구조:
   - ## Summary: 이 심층 분석의 핵심 내용만 3~4줄로 요약. (이모지 금지)
   - ## 심층 분석 (또는 적절한 대제목): 본문은 논리적 흐름에 따라 소제목(###)을 나누어 깊이 있게 작성해.
   - 각 주장이나 정보 뒤에는 반드시 출처를 인용해. 형식: `([출처: 매체명/제목](URL))`
4. ## 결론 (Conclusion): 이 섹션은 반드시 맨 마지막에 포함해. 본문 분석을 바탕으로 실무자(기획자/개발자 등)가 알아야 할 점, 향후 전략적 방향성, 실행 방안 등을 너의 전문적인 통찰력을 더해 도출해 내.
"""

    # [2] 정기 동향 요약용 프롬프트 (스케줄링 실행 시)
    weekly_prompt = f"""
역할: 너는 디지털 접근성 전문 정보 큐레이터이자 전략가야.
제공된 <수집된 웹 자료>를 바탕으로 '주간 디지털 접근성 동향 리포트'를 작성해.

<수집된 웹 자료>
{data_json}
</수집된 웹 자료>

[작성 규칙]
1. 불필요한 정보 제거: 제공된 자료 중 접근성(WCAG, A11y, 포용적 디자인 등)과 관련 없는 내용은 철저히 배제해.
2. 주제별 그룹화: 자료를 단순히 나열하지 말고, 비슷한 주제(예: 법규 및 정책, 기술 및 도구, 가이드라인 업데이트 등)끼리 묶어서 소제목(###)으로 구성해.
3. 환각 금지: 반드시 제공된 자료의 사실에만 기반해.
4. 문서 구조:
   - ## Summary: 이번 동향의 핵심 트렌드를 3~4줄로 요약. (이모지 금지)
   - ## 주간 동향 분석 (또는 적절한 대제목): 그룹화된 주제별로 내용을 서술하며, 정보 뒤에 반드시 출처를 인용해. 형식: `([출처: 매체명/제목](URL))`
   - 각 항목 사이에는 빈 줄을 넣어 가독성을 높여.
5. ## 결론 및 전략 (Conclusion): 이 섹션은 반드시 맨 마지막에 포함해. 이번 동향을 종합하여 실무자들이 주의해야 할 사항, 향후 대응 전략 3가지 이상을 전략적으로 제시해.
"""

    # 모드에 따라 프롬프트 선택
    final_prompt = deep_dive_prompt if is_deep_dive else weekly_prompt

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(
            final_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2, # 논리성과 정확성을 위해 낮춤
                max_output_tokens=8000,
            )
        )
        return response.text
    except Exception as e:
        print(f"✗ Gemini API 오류: {str(e)}")
        sys.exit(1)

def create_blog_post(content: str, title_prefix: str) -> str:
    """마크다운 파일 생성 및 프론트매터 삽입"""
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    time_str = today.strftime('%H%M%S')
    filename = f"a11y-post-{date_str}-{time_str}.md"
    
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
    parser.add_argument('--keywords', nargs='+', help='특정 주제 심층 분석용 키워드 (예: "WCAG 3.0 draft")')
    parser.add_argument('--custom-prompt', type=str, help='Gemini에 전달할 추가 지시사항')
    
    args = parser.parse_args()
    
    is_deep_dive = bool(args.keywords or args.custom_prompt)
    
    print("\n" + "🌐 " * 20)
    print("   디지털 접근성 리포트 자동 생성기")
    print("🌐 " * 20 + "\n")
    
    try:
        # 모드 분리 처리
        if is_deep_dive:
            print("🚀 [심층 분석 모드] 실행 중...")
            search_keywords = args.keywords if args.keywords else ["디지털 접근성"]
            # 심도 있는 문서를 찾기 위해 키워드당 15개의 검색결과를 가져옴
            data = collect_data(search_keywords, max_per_keyword=15)
            title_prefix = f"심층 분석: {', '.join(search_keywords)}"
        else:
            print("📰 [주간 동향 모드] 실행 중...")
            # 다양한 주제를 얕게 훑기 위해 여러 키워드로 검색
            data = collect_data(DEFAULT_WEEKLY_KEYWORDS, max_per_keyword=5)
            title_prefix = "디지털 접근성 주간 동향"
            
        if not data:
            print("⚠️  수집된 웹 데이터가 없습니다.")
            return
            
        # 콘텐츠 생성
        markdown_content = generate_markdown_with_gemini(data, is_deep_dive, args.custom_prompt)
        
        # 파일 저장
        file_path = create_blog_post(markdown_content, title_prefix)
        
        print("="*60)
        print("✅ 블로그 게시물 생성 완료!")
        print("="*60)
        print(f"📄 파일 위치: {file_path}")
        print(f"📊 수집/분석된 웹 문서: {len(data)}개")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  중단되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()