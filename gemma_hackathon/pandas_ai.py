import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv
import os
from data_gathering.test_code.gathering import NaverRECrawler

load_dotenv()


def run(input_query, model, location=None, data=None):
    """
    Run the analysis on real estate data using PandasAI.

    Args:
        input_query (str): User's natural language query
        model (str): Model to use (e.g., "openai")
        location (str, optional): Location to crawl data for (if data not provided)
        data (pd.DataFrame, optional): Existing DataFrame to use

    Returns:
        str: Analysis result
    """
    try:
        # Get data from crawler if not provided
        if data is None and location is not None:
            crawler = NaverRECrawler()
            data = crawler.search_location(location)
        elif data is None:
            raise ValueError("Either location or data must be provided")

        if model == "openai":
            OPENAI_API_KEY = os.getenv("open_ai_api_key")
            llm = OpenAI(api_token=OPENAI_API_KEY)

            # Configure PandasAI
            sdf = SmartDataframe(
                data,
                config={
                    "llm": llm,
                    "verbose": True,
                    "enable_cache": True
                }
            )

            return sdf.chat(input_query)
        else:
            raise ValueError(f"Unsupported model: {model}")

    except Exception as e:
        return f"Error during analysis: {str(e)}"


if __name__ == "__main__":
    # Test functionality
    crawler = NaverRECrawler()
    location = input("검색할 위치를 입력하세요 (예: 강남역): ")
    df = crawler.search_location(location)

    while True:
        test_input = input("원하는 정보 입력 (종료하려면 'q' 입력): ")
        if test_input.lower() == 'q':
            break

        print(f"\nQuery: {test_input}")
        print(run(test_input, "openai", data=df))