IMAGE_GENERATION_PROMPT = """당신은 창의적인 동화 일러스트레이터입니다.
주어진 텍스트를 바탕으로 동화책에 어울리는 이미지를 생성하기 위한 프롬프트를 만들어주세요.

동화 텍스트:
{text}

다음 형식으로 JSON을 생성해주세요:
{{
    "image_prompt": "이미지 생성을 위한 상세한 프롬프트",
    "style": "이미지 스타일 (예: 수채화, 디지털 아트, 만화 등)",
    "key_elements": ["주요 요소1", "주요 요소2", ...],
    "mood": "이미지의 분위기",
    "color_scheme": "색상 구성"
}}

주의사항:
1. 프롬프트는 구체적이고 상세하게 작성해주세요.
2. 동화책의 전체적인 톤과 일관성을 유지해주세요.
3. 주요 요소들을 명확하게 포함시켜주세요.
4. 이미지의 분위기는 텍스트의 감정과 일치하도록 해주세요.
5. 색상 구성은 동화의 분위기에 맞게 설정해주세요.

JSON 형식으로만 응답해주세요."""

# 추가 프롬프트 템플릿들
CHARACTER_VISUAL_PROMPT = """주어진 캐릭터의 시각적 특징을 상세히 설명해주세요:
캐릭터: {character}

다음 형식으로 JSON을 생성해주세요:
{
    "appearance": {
        "face": "얼굴 특징",
        "body": "신체 특징",
        "clothing": "의상 특징"
    },
    "expression": {
        "emotion": "감정",
        "pose": "자세",
        "action": "동작"
    },
    "style": {
        "art_style": "예술 스타일",
        "color_palette": "색상 팔레트",
        "details": "세부 특징"
    }
}"""

SCENE_COMPOSITION_PROMPT = """주어진 장면의 구도를 상세히 설명해주세요:
장면: {scene}

다음 형식으로 JSON을 생성해주세요:
{
    "layout": {
        "perspective": "시점",
        "focus": "초점",
        "balance": "구도 균형"
    },
    "elements": {
        "foreground": "전경 요소",
        "midground": "중경 요소",
        "background": "배경 요소"
    },
    "atmosphere": {
        "lighting": "조명",
        "weather": "날씨",
        "time": "시간대"
    }
}""" 