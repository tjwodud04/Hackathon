from NaverRealEstateHavester.nre.classes import *
from NaverRealEstateHavester.nre.util import *
import requests
import pandas as pd
import urllib.parse


class NaverRECrawler:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def get_coordinates(self, query):
        encoded_query = urllib.parse.quote(query)
        naver_map_url = f"https://map.naver.com/v5/search/{encoded_query}"
        search_url = f"https://map.naver.com/v5/api/search?caller=pcweb&query={encoded_query}&type=all&page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko"

        self.headers["Referer"] = naver_map_url

        try:
            response = requests.get(search_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if (
                    "result" in data
                    and "place" in data["result"]
                    and "list" in data["result"]["place"]
                ):
                    first_result = data["result"]["place"]["list"][0]
                    return NLocation(float(first_result["y"]), float(first_result["x"]))
        except Exception as e:
            print(f"API Error: {str(e)}")

        # 실패 시 하드코딩된 좌표 사용
        default_coordinates = {
            "강남역": (37.4979462, 127.0276206),
            "역삼역": (37.5006, 127.0368),
            "선릉역": (37.5044, 127.0505),
        }

        if query in default_coordinates:
            lat, lon = default_coordinates[query]
            return NLocation(lat, lon)

        raise Exception(f"Location not found for: {query}")

    def search_location(self, query):
        location = self.get_coordinates(query)
        print(f"Searching around coordinates: {location}")
        sector = get_sector(location)
        return self._get_real_estate_data(sector)

    def _get_real_estate_data(self, sector):
        things = get_things_each_direction(sector)
        neighbors = get_all_neighbors(sector)
        update_things_intersection(things, neighbors, get_distance_standard())
        df = pd.DataFrame([t.get_list() for t in things], columns=NThing.HEADER)

        # 가격 단위 변환 (만원 -> 억원)
        price_columns = [
            "minDeal",
            "maxDeal",
            "medianDeal",
            "minLease",
            "maxLease",
            "medianLease",
        ]
        for col in price_columns:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: round(x / 10000, 2) if pd.notnull(x) else x
                )

        return df


if __name__ == "__main__":
    crawler = NaverRECrawler()

    try:
        location = input("검색할 위치를 입력하세요 (예: 강남역): ")
        df = crawler.search_location(location)

        print(f"\n총 {len(df)}개의 매물이 검색되었습니다.")
        print("\n=== 매물 정보 ===")
        columns_to_show = [
            "Name",
            "Type",
            "Build",
            "minDeal",
            "maxDeal",
            "representativeArea",
        ]
        print(df[columns_to_show].head())

        # 파일로 저장
        output_file = f"{location}_real_estate_data.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n데이터가 {output_file}로 저장되었습니다.")

    except Exception as e:
        print(f"Error: {str(e)}")
