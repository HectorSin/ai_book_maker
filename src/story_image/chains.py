from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import RunnableSequence
from config.settings import (
    GPT_MODEL,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    OPENAI_API_KEY,
    IMAGE_SIZE,
    IMAGE_QUALITY,
    IMAGE_GENERATION_TIMEOUT
)
from .prompts import IMAGE_GENERATION_PROMPT
import os
import json
import aiohttp
import asyncio
from typing import Dict, Any

def get_story_image_chain() -> RunnableSequence:
    """Initialize the story image generation chain."""
    llm = ChatOpenAI(
        model_name=GPT_MODEL,
        temperature=0.7,
        max_tokens=1000,
        request_timeout=DEFAULT_TIMEOUT
    )
    
    prompt = PromptTemplate(
        input_variables=["text", "output_dir"],
        template=IMAGE_GENERATION_PROMPT
    )
    
    # 체인 생성 (RunnableSequence 사용)
    chain = prompt | llm
    
    return chain

async def generate_image(prompt: str, output_path: str, max_retries: int = 3) -> str:
    """이미지 생성 함수"""
    from openai import AsyncOpenAI
    
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    for attempt in range(max_retries):
        try:
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1,
                response_format="url"
            )
            
            # 이미지 URL에서 이미지 다운로드
            image_url = response.data[0].url
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        with open(output_path, "wb") as f:
                            f.write(image_data)
                        return output_path
                    else:
                        raise Exception(f"이미지 다운로드 실패: {response.status}")
                        
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"이미지 생성 실패 (시도 {attempt + 1}/{max_retries}): {str(e)}")
            await asyncio.sleep(1)

async def generate_with_retry(chain: RunnableSequence, input_data: Dict[str, Any], max_retries: int = 3) -> str:
    """체인 실행 및 재시도 로직"""
    for attempt in range(max_retries):
        try:
            result = await chain.ainvoke(input_data)
            return result.content
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"체인 실행 실패 (시도 {attempt + 1}/{max_retries}): {str(e)}")
            await asyncio.sleep(1) 