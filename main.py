import argparse
import asyncio
from config.settings import PAGES
from src.pipeline import generate_story

def main():
    parser = argparse.ArgumentParser(description='동화책 생성 파이프라인')
    
    # 기본 설정
    parser.add_argument('--pages', type=int, default=PAGES,
                        help='동화책 페이지 수 (기본값: 5)')
    
    # 동화책 주제 설정
    parser.add_argument('--theme', type=str, default='friendship',
                        help='동화책의 주제 (예: friendship, adventure, courage 등)')
    
    # 대상 연령대 설정
    parser.add_argument('--age-group', type=str, default='children',
                        choices=['toddler', 'children', 'teenager'],
                        help='대상 연령대 (toddler: 유아, children: 어린이, teenager: 청소년)')
    
    # 이미지 생성 설정
    parser.add_argument('--image-style', type=str, default='watercolor',
                        choices=['watercolor', 'digital_art', 'cartoon', 'realistic'],
                        help='이미지 스타일 (watercolor: 수채화, digital_art: 디지털 아트, cartoon: 만화, realistic: 사실적)')
    
    # 출력 설정
    parser.add_argument('--output-dir', type=str, default=None,
                        help='결과물 저장 디렉토리 (기본값: 자동 생성)')
    
    args = parser.parse_args()
    
    print("\n=== 동화책 생성 설정 ===")
    print(f"페이지 수: {args.pages}")
    print(f"주제: {args.theme}")
    print(f"대상 연령대: {args.age_group}")
    print(f"이미지 스타일: {args.image_style}")
    if args.output_dir:
        print(f"출력 디렉토리: {args.output_dir}")
    print("======================\n")
    
    asyncio.run(generate_story(
        pages=args.pages,
        theme=args.theme,
        age_group=args.age_group,
        image_style=args.image_style,
        output_dir=args.output_dir
    ))
    
    print("\n동화책 생성 완료!")

if __name__ == "__main__":
    main()