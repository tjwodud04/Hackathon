import os
import json
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date
from dotenv import load_dotenv


load_dotenv()


class RealEstate(BaseModel):
    item_title: str = Field(..., description="The name of real estate")
    price_type: str = Field(
        ..., description="Contract type of price like 월세, 전세, 매매 etc"
    )
    price: str = Field(..., description="The price of contract for real estate")
    address: str = Field(..., description="The address of real estate")

    build_date: date = Field(..., description="준공 연월")
    direction: str = Field(..., description="방향")


async def extract_real_estate():
    async with AsyncWebCrawler(verbose=True) as crawler:
        while True:
            text = input("입력 :")
            if text == "end":
                break
            result = await crawler.arun(
                url=f"https://new.land.naver.com/search?sk={text}",
                extraction_strategy=LLMExtractionStrategy(
                    provider="openai/gpt-4o",
                    api_token=os.getenv("OPENAI_API_KEY"),
                    schema=RealEstate.schema(),
                    instruction=f"Extract real estate features as following schema",
                ),
                bypass_cache=True,
            )

            print(result.extracted_content)


if __name__ == "__main__":
    # print(RealEstate.schema())
    asyncio.run(extract_real_estate())
