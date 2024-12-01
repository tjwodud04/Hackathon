import pandas as pd
import numpy as np
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv
import os
from data_gathering.test_code.gathering import NaverRECrawler

load_dotenv()


def format_analysis_results(df, query_result):
    """Format analysis results in a clean, readable way"""
    try:
        # Basic statistics
        stats = {
            'total_properties': len(df),
            'unique_properties': df['Name'].nunique(),
            'avg_price': df['MinPrice'].mean(),
            'avg_area': df['Area'].mean(),
            'price_range': (df['MinPrice'].min(), df['MaxPrice'].max())
        }

        # Format the results
        formatted_result = f"""
Real Estate Analysis Summary
==========================

Overview:
---------
• Total Properties: {stats['total_properties']}
• Unique Buildings: {stats['unique_properties']}
• Price Range: {stats['price_range'][0]:.2f} - {stats['price_range'][1]:.2f} million KRW
• Average Price: {stats['avg_price']:.2f} million KRW
• Average Area: {stats['avg_area']:.1f} sqm

Top Properties by Price:
----------------------
{df.nlargest(5, 'MaxPrice')[['Name', 'MinPrice', 'MaxPrice', 'Area']].to_string(index=False)}

Most Affordable Properties:
------------------------
{df.nsmallest(5, 'MinPrice')[['Name', 'MinPrice', 'MaxPrice', 'Area']].to_string(index=False)}

Additional Analysis:
------------------
{query_result if not isinstance(query_result, pd.DataFrame) else ''}

Note: All prices are in millions of KRW and areas in square meters
"""
        return formatted_result
    except Exception as e:
        print(f"Formatting error: {str(e)}")
        return str(query_result)


def run(input_query, model, location=None, data=None):
    """
    Run the analysis on real estate data using PandasAI with enhanced error handling.
    """
    try:
        # Get data from crawler if not provided
        if data is None and location is not None:
            crawler = NaverRECrawler()
            data = crawler.search_location(location)
        elif data is None:
            raise ValueError("Either location or data must be provided")

        # Rename columns for consistency
        column_mapping = {
            'Name': 'Name',
            'minDeal': 'MinPrice',
            'maxDeal': 'MaxPrice',
            'representativeArea': 'Area',
            'Type': 'PropertyType'
        }

        # Select and rename relevant columns
        df = data[list(column_mapping.keys())].copy()
        df.columns = list(column_mapping.values())

        if model == "openai":
            OPENAI_API_KEY = os.getenv("open_ai_api_key")
            if not OPENAI_API_KEY:
                raise ValueError("OpenAI API key not found")

            llm = OpenAI(api_token=OPENAI_API_KEY)

            # Create enhanced prompt
            enhanced_prompt = f"""
            Analyze the real estate data for the following query: {input_query}

            Please provide:
            1. A brief summary of findings
            2. Any specific insights related to the query
            3. Notable properties that match the criteria

            Focus on extracting meaningful insights rather than just listing all properties.
            """

            try:
                sdf = SmartDataframe(
                    df,
                    config={
                        "llm": llm,
                        "verbose": True,
                        "enable_cache": True
                    }
                )

                result = sdf.chat(enhanced_prompt)
                return format_analysis_results(df, result)

            except Exception as chat_error:
                print(f"Chat execution error: {str(chat_error)}")
                # Fallback to basic analysis
                return format_analysis_results(df,
                                               "Unable to perform detailed analysis. Showing basic statistics instead.")

        else:
            raise ValueError(f"Unsupported model: {model}")

    except Exception as e:
        error_msg = f"Analysis error: {str(e)}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    try:
        crawler = NaverRECrawler()
        location = input("Enter location to search (e.g., Gangnam Station): ")
        df = crawler.search_location(location)

        print(f"\nSuccessfully loaded data for {location}")

        while True:
            test_input = input("\nEnter your query (or 'q' to quit): ")
            if test_input.lower() == 'q':
                break

            print("\nAnalyzing your query...")
            result = run(test_input, "openai", data=df)
            print(result)

    except Exception as e:
        print(f"Program error: {str(e)}")