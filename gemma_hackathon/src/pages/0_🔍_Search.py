import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리 설정
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

# 프로젝트 루트를 sys.path에 추가
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from pandas_ai import run

load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="부동산 검색", layout="centered")

# Available locations and predefined queries
LOCATIONS = ["강남역", "서울역", "한강공원", "홍대입구역", "이태원역"]
PREDEFINED_QUERIES = {
    "가격 관련": [
        "3억 이하의 매물을 찾아줘",
        "전세가율이 가장 높은 매물 3개는?",
        "평당 가격이 가장 저렴한 매물은?"
    ],
    "면적/구조 관련": [
        "남향이면서 면적이 넓은 매물 추천",
        "전용면적 20평 이상의 매물 목록",
        "주차장이 있는 매물만 보여줘"
    ],
    "건물 상태 관련": [
        "2010년 이후 지어진 신축 건물만",
        "리모델링이 완료된 매물 찾기",
        "관리상태가 좋은 매물 추천"
    ]
}


def main():
    st.title(":office: 부동산 자연어 검색")

    # Location selector
    selected_location = st.selectbox(
        "검색할 위치를 선택하세요",
        LOCATIONS
    )

    # Query input method selection
    query_method = st.radio(
        "검색 방식을 선택하세요",
        ["직접 입력", "미리 정의된 질문 선택"]
    )

    search_query = ""

    if query_method == "직접 입력":
        search_query = st.text_input(
            "질문을 입력하세요",
            placeholder="예: 남향이면서 면적이 넓은 아파트를 추천해줘"
        )
    else:
        # Category selection
        category = st.selectbox(
            "카테고리를 선택하세요",
            list(PREDEFINED_QUERIES.keys())
        )

        # Query selection from category
        if category:
            search_query = st.selectbox(
                "질문을 선택하세요",
                PREDEFINED_QUERIES[category]
            )

    if st.button("검색") and search_query:
        with st.spinner(f"{selected_location} 데이터 분석 중..."):
            try:
                # Add location context to the query
                contextualized_query = f"{selected_location}의 {search_query}"

                # Call the run function from pandas_ai
                result = run(contextualized_query, "openai", location=selected_location)

                # Display the result
                st.success("검색이 완료되었습니다.")
                st.write("분석 결과:")
                st.write(result)

            except Exception as e:
                st.error(f"검색 중 오류가 발생했습니다: {str(e)}")
                st.write("상세 에러:", e)


if __name__ == "__main__":
    main()