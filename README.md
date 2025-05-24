# AI 동화책 생성기

이 프로젝트는 OpenAI의 GPT와 DALL-E를 활용하여 자동으로 동화책을 생성하는 파이프라인입니다.

## 주요 기능

- 동화책 기본 설정 생성 (등장인물, 교훈, 주제 등)
- 페이지별 내용 구성
- 동화 텍스트 생성
- 이미지 생성 및 텍스트 합성
- 최종 동화책 PDF 생성

## 설치 방법

1. Conda 환경 생성 및 활성화:
```bash
conda env create -f environment.yml
conda activate ai_book
```

## 프로젝트 구조

```
ai_book/
├── config/
│   └── settings.py          # 설정 파일
├── src/
│   ├── story_setting/       # 동화책 기본 설정
│   ├── page_content/        # 페이지별 내용
│   ├── story_text/          # 동화 텍스트
│   ├── story_image/         # 이미지 생성
│   └── pipeline.py          # 메인 파이프라인
├── utils/
│   ├── file_utils.py        # 파일 처리 유틸리티
│   └── image_utils.py       # 이미지 처리 유틸리티
└── main.py                  # 실행 파일
```

## 사용 방법

### 기본 실행
```bash
python main.py
```

### 커스텀 설정으로 실행
```bash
python main.py --pages 10 --theme adventure --age-group teenager --image-style digital_art
```

### 사용 가능한 옵션

- `--pages`: 동화책 페이지 수 (기본값: 5)
- `--theme`: 동화책의 주제 (기본값: friendship)
  - 예: friendship, adventure, courage 등
- `--age-group`: 대상 연령대 (기본값: children)
  - 옵션: toddler, children, teenager
- `--image-style`: 이미지 스타일 (기본값: watercolor)
  - 옵션: watercolor, digital_art, cartoon, realistic
- `--output-dir`: 결과물 저장 디렉토리 (선택사항)

## 생성 과정

1. **동화책 기본 설정 생성**
   - 등장인물, 교훈, 주제, 배경, 톤 등 설정
   - JSON 형식으로 저장

2. **페이지별 내용 구성**
   - 각 페이지의 제목, 요약, 주요 요소 구성
   - 자연스러운 스토리 흐름 유지

3. **동화 텍스트 생성**
   - 각 페이지별 상세 텍스트 생성
   - 대상 연령대에 맞는 문체 사용
   - 한글로 작성

4. **이미지 생성**
   - 텍스트 기반 이미지 프롬프트 생성
   - DALL-E를 통한 이미지 생성
   - 지정된 스타일 적용

5. **최종 동화책 생성**
   - 이미지와 텍스트 합성
   - 페이지별 PDF 생성
   - 전체 동화책 PDF 생성

## 출력 결과

생성된 동화책은 다음과 같은 구조로 저장됩니다:

```
output/
└── storybook_YYYYMMDD_HHMMSS/
    ├── story_setting.json    # 동화책 기본 설정
    ├── page_contents.json    # 페이지별 내용
    ├── page_001/            # 각 페이지별 디렉토리
    │   ├── story.txt        # 페이지 텍스트
    │   ├── generated_image.png  # 생성된 이미지
    │   └── page_data.json   # 페이지 메타데이터
    ├── error_logs/          # 에러 로그 디렉토리
    └── final/               # 최종 동화책 디렉토리
        └── storybook.pdf    # 최종 동화책 PDF
```

## 에러 처리

- JSON 파싱 에러 처리
  - 제어 문자 제거
  - 줄바꿈 문자 통일
  - 파싱 재시도 메커니즘
- 상세한 에러 로깅
  - 각 페이지별 에러 기록
  - 스택 트레이스 저장

## 주의사항

1. OpenAI API 키가 필요합니다.
2. 이미지 생성에는 DALL-E API가 필요합니다.
3. 한글 폰트가 시스템에 설치되어 있어야 합니다.
4. 충분한 디스크 공간이 필요합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 