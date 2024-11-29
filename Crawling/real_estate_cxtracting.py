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

    # Area Information
    min_area: float = Field(..., description="아파트 최소 면적")
    max_area: float = Field(..., description="아파트 최대 면적")
    representative_area: float = Field(..., description="실제 면적")
    floor_area_ratio: float = Field(..., description="용적률")

    # Price Information
    min_deal: int = Field(..., description="최소 가격")
    max_deal: int = Field(..., description="최대 가격")

    # Location Information
    sector: str = Field(..., description="동")
    division: str = Field(..., description="구")

    # Nearby Facilities
    pub_school_count: int = Field(0, description="공립 학교 수")
    pri_school_count: int = Field(0, description="사립 학교 수")
    bus_stop_count: int = Field(0, description="버스 정류장 수")
    metro_count: int = Field(0, description="지하철 수")
    preschool_count: int = Field(0, description="유치원 수")
    hospital_count: int = Field(0, description="병원 수")
    parking_count: int = Field(0, description="주차장 수")
    mart_count: int = Field(0, description="마트 수")
    convenience_store_count: int = Field(0, description="편의점 수")
    office_count: int = Field(0, description="관공서 수")


async def extract_real_estate(text):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=f"https://new.land.naver.com/search?sk={text}",
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o",
                api_token=os.getenv("OPENAI_API_KEY"),
                schema=RealEstate.schema(),
                instruction=f"Extract item_title, price_type and price for real estate from the page.",
            ),
            bypass_cache=True,
        )

    print(result.extracted_content)


if __name__ == "__main__":
    print(RealEstate.schema())
    # asyncio.run(extract_real_estate(text="강남역"))
