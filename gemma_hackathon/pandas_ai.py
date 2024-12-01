import pandas as pd
#import numpy as np
#from pandasai import smart_dataframe#,PandasAI
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
#from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

csv_path = '../Crawling/강남역_real_estate_data.csv'
csv = pd.read_csv(csv_path)
#check
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

def run(input, model, data = csv):
    
    if model == "openai":
        OPENAI_API_KEY = os.getenv('open_ai_api_key')
        llm = OpenAI(api_token=OPENAI_API_KEY)


    sdf = SmartDataframe(csv, config={"llm": llm})

    #pandas_ai = PandasAI(llm, verbose=True)
    #pandas_ai.run(sdf, prompt=input) #csv : called l7
    print(sdf.chat(input) )
    #return 

if __name__ == "__main__":
    test_model = "openai"
    test_input = "give only five name of apt where representativeArea is larger then 50 odered by price" #단위 등 데이터 후처리 필요.
    print(f"{test_input}")

    run(test_input, test_model)
