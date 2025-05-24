from PIL import Image, ImageDraw, ImageFont
import os

def create_final_page(image_path: str, text: str, output_path: str, font_size: int = 40) -> str:
    """이미지와 텍스트를 합성하여 최종 페이지를 생성합니다."""
    # 원본 이미지 로드
    image = Image.open(image_path)
    width, height = image.size
    
    # 텍스트 영역 높이 계산 (이미지 높이의 1/3)
    text_height = height // 3
    
    # 새로운 이미지 생성 (원본 이미지 + 텍스트 영역)
    final_image = Image.new('RGB', (width, height + text_height), 'white')
    
    # 원본 이미지 붙이기
    final_image.paste(image, (0, 0))
    
    # 텍스트 영역에 텍스트 그리기
    draw = ImageDraw.Draw(final_image)
    
    # 폰트 설정 (한글 지원 폰트 사용)
    try:
        font = ImageFont.truetype("malgun.ttf", font_size)  # Windows의 기본 한글 폰트
    except:
        font = ImageFont.load_default()
    
    # 텍스트 줄바꿈 처리
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_width = draw.textlength(' '.join(current_line), font=font)
        if line_width > width - 40:  # 좌우 여백 20px씩
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(' '.join(current_line))
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # 텍스트 그리기
    y = height + 20  # 상단 여백
    for line in lines:
        # 텍스트 중앙 정렬
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) // 2
        draw.text((x, y), line, font=font, fill='black')
        y += font_size + 10  # 줄 간격
    
    # 결과 저장
    final_image.save(output_path)
    return output_path

def create_final_storybook(output_dir: str, pages: int) -> str:
    """최종 동화책 페이지들을 생성합니다."""
    # 완성본 디렉토리 생성
    final_dir = os.path.join(output_dir, "final")
    os.makedirs(final_dir, exist_ok=True)
    
    # 각 페이지 처리
    for page_num in range(1, pages + 1):
        page_dir = os.path.join(output_dir, f"page_{page_num:03d}")
        
        # 원본 이미지와 텍스트 파일 경로
        image_path = os.path.join(page_dir, "generated_image.png")
        text_path = os.path.join(page_dir, "story.txt")
        
        if os.path.exists(image_path) and os.path.exists(text_path):
            # 텍스트 읽기
            with open(text_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 최종 페이지 생성
            output_path = os.path.join(final_dir, f"page_{page_num:03d}.png")
            create_final_page(image_path, text, output_path)
    
    return final_dir 