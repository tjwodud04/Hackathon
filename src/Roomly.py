import streamlit as st

st.set_page_config(
    page_title="부동산 AI 검색 서비스",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 사이드바 네비게이션
st.sidebar.title("부동산 AI 검색")
demo_section = st.sidebar.radio(
    "메뉴",
    [
        "서비스 소개",
        "주요 기능",
        "기술 스택",
        "시스템 설계",
        "문제 해결 접근",
        "사용자 후기",
        "서비스 장점",
        "문의하기",
    ],
)

# 메인 컨텐츠
st.title("AI 기반 부동산 검색 서비스")
st.subheader("인공지능으로 스마트한 부동산 검색을")

if demo_section == "서비스 소개":
    st.header("서비스 소개")
    st.write(
        """
    AI 기반 부동산 검색 서비스는 최신 자연어 처리와 머신러닝 기술을 활용하여 
    부동산 검색 경험을 혁신적으로 개선합니다.

    복잡한 부동산 정보를 쉽게 검색하고 분석할 수 있도록 도와주며,
    사용자의 요구사항에 맞는 최적의 매물을 추천해드립니다.
    """
    )

    st.image("assets/overview.png", caption="서비스 개요")

elif demo_section == "주요 기능":
    st.header("주요 기능")

    features = {
        "스마트 검색": "자연어 기반 검색으로 원하는 조건의 매물을 쉽게 찾기",
        "매물 데이터베이스": "실시간 업데이트되는 매물 정보와 상세 필터링",
        "시세 분석": "지역별, 유형별 시세 동향 분석 및 예측",
        "위치 기반 서비스": "교통, 편의시설 등 주변 인프라 정보 제공",
        "AI 챗봇 상담": "24시간 가능한 AI 기반 부동산 상담 서비스",
        "매물 비교 분석": "선택한 매물들의 상세 비교 분석 기능",
    }

    for feature, description in features.items():
        st.subheader(feature)
        st.write(description)

elif demo_section == "기술 스택":
    st.header("기술 스택")

    st.write(
        """
    최신 기술을 활용한 안정적이고 효율적인 서비스 제공:

    1. Python: 백엔드 개발 및 데이터 처리
    2. Streamlit: 웹 인터페이스 구현
    3. OpenAI API: 자연어 처리 및 AI 챗봇
    4. MongoDB: 부동산 데이터 저장 및 관리
    5. Pandas: 데이터 분석 및 처리
    6. GeoPy: 위치 기반 서비스 구현
    7. Plotly: 데이터 시각화
    8. 공공데이터 API: 부동산 실거래가 정보 연동
    """
    )

elif demo_section == "시스템 설계":
    st.header("시스템 설계")

    st.subheader("1. 데이터 수집 시스템")
    st.write(
        """
    - 실시간 매물 정보 수집
    - 공공데이터 연동
    - 사용자 피드백 데이터 수집
    """
    )

    st.subheader("2. AI 분석 엔진")
    st.write(
        """
    - 자연어 처리 기반 검색 시스템
    - 추천 알고리즘
    - 가격 예측 모델
    """
    )

    st.subheader("3. 사용자 인터페이스")
    st.write(
        """
    - 반응형 웹 디자인
    - 직관적인 검색 필터
    - 실시간 업데이트
    """
    )

elif demo_section == "문제 해결 접근":
    st.header("문제 해결 접근")

    st.subheader("데이터 품질 관리")
    st.write(
        """
    - 실시간 데이터 검증
    - 중복 매물 필터링
    - 가격 이상치 탐지
    """
    )

    st.subheader("사용자 경험 최적화")
    st.write(
        """
    - 검색 결과 정확도 향상
    - 응답 시간 최적화
    - 직관적인 UI/UX 설계
    """
    )

elif demo_section == "사용자 후기":
    st.header("사용자 후기")

    stories = [
        {
            "title": "첫 내 집 마련 성공",
            "story": """
            AI 검색 서비스를 통해 제가 원하는 조건에 맞는 아파트를 쉽게 찾을 수 있었어요.
            주변 시세와 비교해서 합리적인 가격에 구매할 수 있었습니다.
            """,
        },
        {
            "title": "투자자의 선택",
            "story": """
            시세 분석과 예측 기능이 투자 결정에 큰 도움이 되었습니다.
            여러 지역의 매물을 한눈에 비교할 수 있어서 좋았어요.
            """,
        },
        {
            "title": "부동산 중개인의 필수 도구",
            "story": """
            AI 챗봇이 기본적인 문의를 처리해주어 업무 효율이 크게 향상되었습니다.
            매물 관리도 훨씬 수월해졌어요.
            """,
        },
    ]

    for story in stories:
        st.subheader(story["title"])
        st.write(story["story"])

elif demo_section == "서비스 장점":
    st.header("서비스 장점")

    st.write(
        """
    1. 정확한 정보: 실시간 업데이트되는 검증된 매물 정보

    2. 스마트 검색: AI 기반 맞춤형 매물 추천

    3. 편리한 인터페이스: 누구나 쉽게 사용할 수 있는 직관적인 디자인

    4. 상세 분석: 지역별 시세 분석과 미래 가치 예측

    5. 통합 정보: 부동산 정보와 주변 인프라 정보를 한번에 확인
    """
    )

elif demo_section == "문의하기":
    st.header("서비스 문의")

    st.write(
        """
    더 나은 부동산 거래를 위한 첫 걸음을 시작하세요.

    문의 방법:

    1. 📱 전화 문의: 02-XXX-XXXX
    2. 📧 이메일: contact@realestate.ai
    3. 💬 카카오톡: @부동산AI

    부동산 거래의 새로운 패러다임을 경험해보세요.
    """
    )

    st.button("문의하기")
    st.button("서비스 신청")

# 푸터
st.sidebar.markdown("---")
st.sidebar.info("부동산 AI 검색 서비스 - 더 스마트한 부동산 거래")
st.sidebar.text("© 2024 부동산 AI 팀")