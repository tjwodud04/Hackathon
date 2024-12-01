import pandas as pd

# import numpy as np
# from pandasai import smart_dataframe#,PandasAI
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

# from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
from data_gathering.test_code.test import NaverRECrawler

load_dotenv()


csv_path = "/Users/jeonmingyu/hackathon/IBM_Watson_Assistant/IBM_Hackathon/gemma_hackathon/data_gathering/data/강남역_real_estate_data.xlsx"
csv = pd.read_excel(csv_path)


# check
"""
>>> csv.columns
Index(['Name', 'Type', 'Build', 'Dir', 'minArea', 'maxArea',
       'representativeArea', 'floorAreaRatio', 'minDeal', 'maxDeal',
       'medianDeal', 'minLease', 'maxLease', 'medianLease', 'minDealUnit',
       'maxDealUnit', 'medianDealUnit', 'minLeaseUnit', 'maxLeaseUnit',
       'medianLeaseUnit', 'Lat', 'Lon', 'BUS', 'METRO', 'INFANT', 'PRESCHOOL',
       'HOSPITAL', 'PARKING', 'MART', 'CONVENIENCE', 'WASHING', 'BANK',
       'OFFICE', 'PRI_SCHOOL', 'PUB_SCHOOL'],
      dtype='object')

      
      
>>> csv['Type'].unique()
array(['APT', 'OPST'], dtype=object)      

Build : 건축 일자 (년년년년월월) #애매해서 이름 바꿈
    
>>> csv['Dir'].unique()
array(['EE', 'ES', 'WW', 'WS', 'SS', 'EN', 'NN', 'WN'], dtype=object)

representativeArea : 실제면적


"""


def run(input, model, data=csv):

    if model == "openai":
        OPENAI_API_KEY = os.getenv("open_ai_api_key")
        llm = OpenAI(api_token=OPENAI_API_KEY)

    sdf = SmartDataframe(csv, config={"llm": llm})

    # pandas_ai = PandasAI(llm, verbose=True)
    # pandas_ai.run(sdf, prompt=input) #csv : called l7
    return sdf.chat(input)
    # print(sdf.chat(input) )

    # return


if __name__ == "__main__":
    crawler = NaverRECrawler()
    location = input("검색할 위치를 입력하세요 (예: 강남역): ")
    df = crawler.search_location(location)
    while True:
        test_model = "openai"
        test_input = input("원하는 정보 입력 : ")  # 단위 등 데이터 후처리 필요.
        print(f"{test_input}")
        print(run(test_input, test_model, data=df))
