import os
import asyncio
import aiohttp
import json
import traceback
import datetime
import time
import re
from PIL import Image

# SETTING
from config.settings import OUTPUT_DIR, MAX_CONCURRENT

# MODULE
from src.story_setting.chains import get_story_setting_chain
from src.page_content.chains import get_page_content_chain
from src.story_text.chains import get_story_text_chain
from src.story_image.chains import get_story_image_chain, generate_image

# UTIL
from utils.file_utils import ensure_dir_exists, create_csv_log, get_unique_dirname
from utils.image_utils import create_final_storybook

def clean_json_string(json_str: str) -> str:
    """JSON 문자열에서 제어 문자를 제거하고 이스케이프 처리합니다."""
    # 제어 문자 제거
    json_str = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', json_str)
    # 줄바꿈을 \n으로 통일
    json_str = json_str.replace('\r\n', '\\n').replace('\r', '\\n').replace('\n', '\\n')
    return json_str

def safe_json_loads(json_str: str, max_retries: int = 3) -> dict:
    """JSON 문자열을 안전하게 파싱합니다."""
    for attempt in range(max_retries):
        try:
            # JSON 문자열 정리
            cleaned_str = clean_json_string(json_str)
            return json.loads(cleaned_str)
        except json.JSONDecodeError as e:
            if attempt == max_retries - 1:
                raise
            print(f"JSON 파싱 재시도 {attempt + 1}/{max_retries}")
            # 마지막 시도에서도 실패하면 원본 에러를 발생시킴
            if attempt == max_retries - 2:
                print(f"원본 JSON 문자열: {json_str}")
                print(f"정리된 JSON 문자열: {cleaned_str}")
    return {}

async def generate_story(pages: int, theme: str = "friendship", age_group: str = "children", 
                        image_style: str = "watercolor", output_dir: str = None):
    """동화책 생성 메인 파이프라인"""
    start_time = time.time()
    
    # 출력 디렉토리 생성 (중복되지 않는 이름으로)
    if output_dir is None:
        output_dir = os.path.join(OUTPUT_DIR, f"storybook_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
        output_dir = get_unique_dirname(output_dir)
    ensure_dir_exists(output_dir)

    # 에러 로그를 저장할 디렉토리 생성
    error_log_dir = os.path.join(output_dir, "error_logs")
    ensure_dir_exists(error_log_dir)
    
    # 에러 카운터 초기화
    error_counters = {
        'total_errors': 0,
        'setting_errors': 0,
        'content_errors': 0,
        'text_errors': 0,
        'image_errors': 0,
    }

    try:
        # 1. 동화책 기본 설정 (등장인물, 교훈)
        print("1. 동화책 기본 설정 생성 중...")
        story_setting_chain = get_story_setting_chain()
        story_setting = await story_setting_chain.ainvoke({
            "theme": theme,
            "age_group": age_group
        })
        story_setting = safe_json_loads(story_setting.content)
        
        # 설정 저장
        with open(os.path.join(output_dir, "story_setting.json"), "w", encoding="utf-8") as f:
            json.dump(story_setting, f, ensure_ascii=False, indent=2)
        
        # 2. 페이지별 내용 구성
        print("2. 페이지별 내용 구성 중...")
        page_content_chain = get_page_content_chain()
        page_contents = await page_content_chain.ainvoke({
            "pages": pages,
            "setting": json.dumps(story_setting, ensure_ascii=False)
        })
        page_contents = safe_json_loads(page_contents.content)
        
        # 페이지 내용 저장
        with open(os.path.join(output_dir, "page_contents.json"), "w", encoding="utf-8") as f:
            json.dump(page_contents, f, ensure_ascii=False, indent=2)
        
        # 3. 각 페이지별 상세 내용 및 이미지 생성
        print("3. 페이지별 상세 내용 및 이미지 생성 중...")
        story_text_chain = get_story_text_chain()
        story_image_chain = get_story_image_chain()
        
        async with aiohttp.ClientSession() as session:
            for page in page_contents["pages"]:
                page_num = page["page_number"]
                print(f"\n페이지 {page_num}/{pages} 처리 중...")
                
                try:
                    # 페이지별 결과 저장 디렉토리
                    page_dir = os.path.join(output_dir, f"page_{page_num:03d}")
                    ensure_dir_exists(page_dir)
                    
                    # 3-1. 페이지 텍스트 생성
                    print(f"  - 페이지 {page_num} 텍스트 생성 중...")
                    story_text_result = await story_text_chain.ainvoke({
                        "content": json.dumps(page, ensure_ascii=False),
                        "setting": json.dumps(story_setting, ensure_ascii=False),
                        "age_group": age_group
                    })
                    story_text_data = safe_json_loads(story_text_result.content)
                    
                    # 텍스트 저장
                    with open(os.path.join(page_dir, "story.txt"), "w", encoding="utf-8") as f:
                        f.write(story_text_data["story_text"])
                    
                    # 3-2. 페이지 이미지 생성
                    print(f"  - 페이지 {page_num} 이미지 생성 중...")
                    image_prompt_result = await story_image_chain.ainvoke({
                        "text": story_text_data["story_text"],
                        "output_dir": page_dir,
                        "style": image_style
                    })
                    image_prompt_data = safe_json_loads(image_prompt_result.content)
                    
                    # 이미지 생성 및 저장
                    image_path = os.path.join(page_dir, "generated_image.png")
                    await generate_image(image_prompt_data["image_prompt"], image_path)
                    
                    # 결과 데이터 저장
                    result_data = {
                        "page_number": page_num,
                        "content": page,
                        "story_text": story_text_data,
                        "image_prompt": image_prompt_data,
                        "image_path": image_path
                    }
                    
                    with open(os.path.join(page_dir, "page_data.json"), "w", encoding="utf-8") as f:
                        json.dump(result_data, f, ensure_ascii=False, indent=2)
                        
                except Exception as e:
                    error_msg = f"페이지 {page_num} 처리 중 에러: {str(e)}"
                    print(error_msg)
                    error_counters['total_errors'] += 1
                    
                    # 에러 로그 저장
                    error_log_path = os.path.join(error_log_dir, f"page_{page_num}_error.txt")
                    with open(error_log_path, "w", encoding="utf-8") as f:
                        f.write(f"페이지: {page_num}\n")
                        f.write(f"에러: {str(e)}\n")
                        f.write(f"스택 트레이스:\n{traceback.format_exc()}\n")
                        f.write(f"시간: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 4. 최종 결과물 체크
        print("\n4. 최종 결과물 체크 중...")
        check_results(output_dir, pages, error_counters)
        
        # 5. 최종 동화책 생성
        print("\n5. 최종 동화책 생성 중...")
        final_dir = create_final_storybook(output_dir, pages)
        
        # 최종 통계 출력
        print("\n=== 동화책 생성 결과 ===")
        print(f"총 페이지 수: {pages}")
        print(f"주제: {theme}")
        print(f"대상 연령대: {age_group}")
        print(f"이미지 스타일: {image_style}")
        print(f"총 에러 수: {error_counters['total_errors']}")
        print(f"처리가 완료되었습니다. 결과물은 {output_dir}에 저장되었습니다.")
        print(f"최종 동화책은 {final_dir}에 저장되었습니다.")
        print(f"총 처리 시간: {time.time() - start_time:.2f}초")
        print("======================")
        
    except Exception as e:
        print(f"동화책 생성 중 에러 발생: {str(e)}")
        print(traceback.format_exc())

def check_results(output_dir, pages, error_counters):
    """생성된 결과물 체크"""
    try:
        # 각 페이지별 결과물 존재 여부 확인
        for page_num in range(1, pages + 1):
            page_dir = os.path.join(output_dir, f"page_{page_num:03d}")
            if not os.path.exists(page_dir):
                print(f"경고: 페이지 {page_num} 디렉토리가 없습니다.")
                continue
                
            # 필수 파일 체크
            required_files = ["story.txt", "page_data.json", "generated_image.png"]
            for file in required_files:
                file_path = os.path.join(page_dir, file)
                if not os.path.exists(file_path):
                    print(f"경고: 페이지 {page_num}의 {file}이(가) 없습니다.")
                    
    except Exception as e:
        print(f"결과물 체크 중 에러: {str(e)}")
        raise