import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

async def extract_openai_pricing():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/",
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o",
                api_token=os.getenv("OPENAI_API_KEY"),
                schema=OpenAIModelFee.schema(),
                extraction_type="schema",
                instruction="just show me all of things"
            ),
            bypass_cache=True
        )
        print(result.extracted_content)



async def search_naver_real_estate(keyword: str):
    async with AsyncWebCrawler(headless=True) as crawler:
        # 검색 키워드 파라미터를 포함한 URL 생성
        base_url = "https://new.land.naver.com/api/complexes/list"
        params = {
            "keyword": keyword,
            "region": "1100000000",  # 서울 지역 예시
            "realEstateType": "A01",  # 매물 유형: 아파트 (필요시 변경 가능)
            "tradeType": "B1",       # 매매 (필요시 전세/월세로 변경 가능)
        }
        search_url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

        # 페이지 크롤링 시작
        page = await crawler.arun(url=search_url)

        # 검색 결과를 가져오기 위한 데이터 추출
        # results = await page.validate("""
        # () => {
        #     const data = JSON.parse(document.body.innerText);  // JSON 데이터 로드
        #     return data.complexList.map(item => ({
        #         name: item.name || 'No name',
        #         price: item.tradePrice || 'No price'
        #     }));
        # }
        # """)
        print(page)
        # # 결과 출력
        # for result in results:
        #     print(f"Name: {result['name']}, Price: {result['price']}")

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url="https://new.land.naver.com/search?ms=37.4924968,127.0306422,18&a=OPST:PRE&b=B2&d=70&e=RETAIL&g=10000&j=10",
            bypass_cache=True,
            simulate_user=True,  # Causes random mouse movements and clicks
            override_navigator=True,  # Makes the browser appear more like a real user
            chunking_strategy=RegexChunking(patterns=["\n\n"]),
        )


        print(result.markdown)  # Print first 500 characters



class RealEstate(BaseModel):
    item_title: str = Field(..., description="The name of real estate")
    price_type: str = Field(..., description="Contract type of price like 월세, 전세, 매매 etc")
    price: str = Field(..., description="The price of contract for real estate")

async def extract_real_estate(text):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=f"https://new.land.naver.com/search?sk={text}",
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o",
                api_token=os.getenv('OPENAI_API_KEY'),
                schema=RealEstate.schema(),
                instruction=f"Extract item_title, price_type and price for real estate from the page."
            ),
            bypass_cache=True,
        )

    tech_content = json.loads(result.extracted_content)
    print(tech_content)


if __name__ == "__main__":
    asyncio.run(extract_real_estate(text = "강남역"))
   