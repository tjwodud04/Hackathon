import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

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

    print(result.extracted_content)
    tech_content = json.loads(result.extracted_content)
    print(tech_content)


if __name__ == "__main__":
    asyncio.run(extract_real_estate(text = "강남역"))