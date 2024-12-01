import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from st_aggrid import AgGrid, GridOptionsBuilder
import time
from llm import run

load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="Real Estate Search", layout="centered")


# Function to load the real estate database
def load_database():
    csv_path = '../Crawling/강남역_real_estate_data.csv'
    return pd.read_csv(csv_path)


# Function to truncate text
def truncate_text(text, max_words=50):
    if text is None or text == "":
        return "N/A"
    words = str(text).split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return text


def load_table(all_data):
    display_df = pd.DataFrame(all_data)
    gb = GridOptionsBuilder.from_dataframe(display_df)

    # Configure columns
    gb.configure_default_column(
        wrapText=True,
        autoHeight=True,
        maxWidth=500,
        groupable=True,
        cellStyle={"white-space": "pre-wrap"},
        sortable=True
    )

    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar(filters_panel=True, columns_panel=True)

    gridOptions = gb.build()

    AgGrid(
        display_df,
        gridOptions=gridOptions,
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=True,
        height=500,
        theme="streamlit",
        key="ag_grid_" + str(time.time()),
    )


def main():
    st.title("🏢 부동산 검색")

    # Load the data
    df = load_database()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        property_type = st.selectbox("부동산 유형", ["전체"] + list(df['Type'].unique()))

    with col2:
        min_area = st.number_input("최소 면적", min_value=float(df['representativeArea'].min()))

    with col3:
        max_area = st.number_input("최대 면적", min_value=float(df['representativeArea'].min()),
                                   value=float(df['representativeArea'].max()))

    # Search using LLM
    search_query = st.text_input("검색어를 입력하세요", "")

    if st.button("검색"):
        with st.spinner("검색 중..."):
            if search_query:
                try:
                    # Use the LLM for search
                    llm_results = run(search_query, "openai", df)
                    st.success("검색이 완료되었습니다.")
                    st.write("LLM 검색 결과:", llm_results)
                except Exception as e:
                    st.error(f"검색 중 오류가 발생했습니다: {str(e)}")

    # Filter the data
    filtered_data = df.copy()
    if property_type != "전체":
        filtered_data = filtered_data[filtered_data['Type'] == property_type]
    filtered_data = filtered_data[
        (filtered_data['representativeArea'] >= min_area) &
        (filtered_data['representativeArea'] <= max_area)
        ]

    # Display results
    st.subheader("검색 결과")

    # Prepare display data
    display_data = []
    for _, row in filtered_data.iterrows():
        display_data.append({
            "이름": row['Name'],
            "유형": row['Type'],
            "건축일자": row['Build'],
            "방향": row['Dir'],
            "면적": row['representativeArea'],
            "용적률": row['floorAreaRatio'],
            "매매가(중간값)": row['medianDeal'],
            "전세가(중간값)": row['medianLease'],
            "위도": row['Lat'],
            "경도": row['Lon'],
            "지하철": row['METRO'],
            "주차": row['PARKING'],
            "편의점": row['CONVENIENCE']
        })

    load_table(display_data)

    # Optional: Add a map
    if st.checkbox("지도로 보기"):
        st.map(filtered_data[['Lat', 'Lon']])


if __name__ == "__main__":
    main()