from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from .prompts import STORY_SETTING_PROMPT
from config.settings import GPT_MODEL, DEFAULT_TIMEOUT, MAX_RETRIES, RETRY_DELAY
import asyncio

def get_story_setting_chain():
    """동화책의 기본 설정(등장인물, 교훈)을 생성하는 체인"""
    
    # LLM 모델 초기화
    llm = ChatOpenAI(
        model_name=GPT_MODEL,
        temperature=0.7,
        max_tokens=1000,
        request_timeout=DEFAULT_TIMEOUT
    )
    
    # 프롬프트 템플릿 생성
    prompt = PromptTemplate(
        input_variables=["theme", "age_group"],
        template=STORY_SETTING_PROMPT
    )
    
    # 체인 생성 (RunnableSequence 사용)
    chain = prompt | llm
    
    return chain

async def generate_with_retry(chain, **kwargs):
    """재시도 로직이 포함된 체인 실행"""
    for attempt in range(MAX_RETRIES):
        try:
            result = await chain.ainvoke(kwargs)
            return result.content
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise e
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            await asyncio.sleep(RETRY_DELAY) 