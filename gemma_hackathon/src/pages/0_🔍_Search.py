import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Set project root directory
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from pandas_ai import run

load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="Real Estate Search", layout="centered")

# Available locations and predefined queries
LOCATIONS = ["Gangnam Station", "Seoul Station", "Hangang Park", "Hongdae Station", "Itaewon Station"]
LOCATION_MAPPING = {
    "Gangnam Station": "강남역",
    "Seoul Station": "서울역",
    "Hangang Park": "한강공원",
    "Hongdae Station": "홍대입구역",
    "Itaewon Station": "이태원역"
}

PREDEFINED_QUERIES = {
    "Price Related": [
        "Find properties under 300 million won",
        "What are the top 3 properties with lowest monthly rent?",
        "Which property has the lowest price per square meter?"
    ],
    "Area/Structure Related": [
        "Recommend properties facing south with large area",
        "List properties with more than 66㎡ (20 pyeong)",
        "Show only properties with parking spaces"
    ],
    "Building Condition": [
        "Show buildings constructed after 2010",
        "Find properties that have been renovated",
        "Recommend properties in good maintenance condition"
    ]
}


def initialize_session_state():
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None


def main():
    initialize_session_state()

    st.title(":office: Real Estate Natural Language Search")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Location selector
        selected_location_eng = st.selectbox(
            "Select Location",
            LOCATIONS
        )
        selected_location = LOCATION_MAPPING[selected_location_eng]

        # Query input method selection
        query_method = st.radio(
            "Choose Search Method",
            ["Direct Input", "Predefined Questions"]
        )

        search_query = ""

        if query_method == "Direct Input":
            search_query = st.text_input(
                "Enter your question",
                placeholder="Example: Recommend properties facing south with large area"
            )
        else:
            # Category selection
            category = st.selectbox(
                "Select Category",
                list(PREDEFINED_QUERIES.keys())
            )

            # Query selection from category
            if category:
                search_query = st.selectbox(
                    "Select Question",
                    PREDEFINED_QUERIES[category]
                )

    with col2:
        st.subheader("Search History")
        if st.session_state.search_history:
            for idx, (loc, query, time) in enumerate(st.session_state.search_history[-5:]):
                st.text(f"{time}\n{loc}: {query}")
        else:
            st.text("No search history yet")

    if st.button("Search"):
        if search_query:
            with st.spinner(f"Analyzing data for {selected_location_eng}..."):
                try:
                    # Add location context to the query
                    contextualized_query = f"For {selected_location_eng} ({selected_location}): {search_query}"

                    # Call the run function from pandas_ai
                    result = run(contextualized_query, "openai", location=selected_location)

                    # Update search history
                    from datetime import datetime
                    st.session_state.search_history.append((
                        selected_location_eng,
                        search_query,
                        datetime.now().strftime("%H:%M:%S")
                    ))

                    # Display the result
                    st.success("Search completed")

                    # Create result display container
                    result_container = st.container()
                    with result_container:
                        st.write("### Analysis Results")
                        st.write(result)

                    # Add options for new search
                    st.write("---")
                    st.write("Would you like to:")
                    col3, col4 = st.columns(2)
                    with col3:
                        if st.button("Start New Search"):
                            st.experimental_rerun()
                    with col4:
                        if st.button("Modify Current Search"):
                            st.session_state.current_data = result

                except Exception as e:
                    st.error(f"Search error occurred: {str(e)}")
                    st.write("Detailed error:", e)

    # Footer with instructions
    st.markdown("---")
    st.markdown("""
    **Tips for searching:**
    - Be specific about what you're looking for
    - You can mention price ranges, area preferences, or building conditions
    - Use the predefined questions for common queries
    """)


if __name__ == "__main__":
    main()