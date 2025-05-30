PAGE_CONTENT_PROMPT = """당신은 창의적인 동화 작가입니다.
주어진 설정을 바탕으로 {pages}페이지 분량의 동화책 내용을 구성해주세요.

동화 설정:
{setting}

다음 형식으로 JSON을 생성해주세요:
{{
    "pages": [
        {{
            "page_number": 1,
            "title": "페이지 제목",
            "summary": "페이지 내용 요약",
            "key_elements": ["주요 요소1", "주요 요소2", ...]
        }},
        // ... {pages}개의 페이지
    ]
}}

주의사항:
1. 각 페이지는 자연스럽게 이어지도록 구성해주세요.
2. 페이지 제목은 간단하고 매력적으로 해주세요.
3. 내용 요약은 2-3문장으로 핵심을 전달해주세요.
4. 주요 요소는 해당 페이지에서 중요한 내용이나 이미지로 표현할 요소들을 나열해주세요.
5. 마지막 페이지는 이야기를 자연스럽게 마무리해주세요.

JSON 형식으로만 응답해주세요."""

# 추가 프롬프트 템플릿들
PAGE_TRANSITION_PROMPT = """주어진 두 페이지 간의 자연스러운 연결을 만들어주세요:
이전 페이지: {previous_page}
다음 페이지: {next_page}

다음 형식으로 JSON을 생성해주세요:
{{
    "transition_type": "연결 유형 (예: 시간 경과, 장소 이동, 감정 변화 등)",
    "transition_text": "연결을 위한 짧은 문장",
    "connection_points": ["연결점1", "연결점2"]
}}"""

PAGE_DETAIL_PROMPT = """주어진 페이지의 상세 내용을 생성해주세요:
페이지 요약: {page_summary}

다음 형식으로 JSON을 생성해주세요:
{{
    "main_scene": "주요 장면 설명",
    "dialogue": ["대화1", "대화2"],
    "descriptions": ["묘사1", "묘사2"],
    "emotions": ["감정1", "감정2"]
}}""" 