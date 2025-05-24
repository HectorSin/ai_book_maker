import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")  # Stable Diffusion API 키

# 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
INPUT_DIR = os.path.join(BASE_DIR, "input")

# 모델 설정
GPT_MODEL = "gpt-4"  # GPT 모델
STABLE_DIFFUSION_MODEL = "stable-diffusion-xl-1024-v1-0"  # Stable Diffusion 모델

# 이미지 생성 설정
IMAGE_SIZE = "1024x1024"  # DALL-E 3 지원 크기: 1024x1024, 1792x1024, 1024x1792
IMAGE_STYLE = "children's book illustration"  # 이미지 스타일
IMAGE_QUALITY = "standard"  # standard 또는 hd
IMAGE_GENERATION_TIMEOUT = 60  # 초

# 동시 처리 설정
MAX_CONCURRENT = 3  # 최대 동시 처리 수
BATCH_SIZE = 5  # 배치 크기

# 타임아웃 설정
DEFAULT_TIMEOUT = 60  # API 요청 타임아웃(초)

# 재시도 설정
MAX_RETRIES = 3  # 최대 재시도 횟수
RETRY_DELAY = 2  # 재시도 간격(초)

# 출력 설정
STORY_SETTING_FILE = "story_setting.json"
PAGE_CONTENTS_FILE = "page_contents.json"
ERROR_LOG_DIR = "error_logs"

PAGES = 5