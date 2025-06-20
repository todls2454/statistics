import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 다국어 지원
LANGUAGES = {
    "한국어": {
        "title": "🏘️ 빈집 활용 대시보드",
        "filter_header": "📌 필터 조건을 선택하세요",
        "language": "언어 선택",
        "city_select": "🏙️ 지역 선택",
        "max_hospital": "🏥 병원까지 최대 거리",
        "max_school": "🏫 학교까지 최대 거리",
        "max_industry": "🏢 직장까지 최대 거리",
        "max_price": "💰 최대 예상 가격 (만원)",
        "user_type": "👥 사용자 유형",
        "property_conditions": "🏠 건물 조건",
        "area_filter": "면적 조건 (㎡)",
        "room_filter": "방 개수",
        "bathroom_filter": "욕실 개수",
        "floor_filter": "건물 층수",
        "tab1": "🗺️ 지도 보기",
        "tab2": "💰 가격 비교",
        "tab3": "📋 상세 테이블",
        "tab4": "🏠 건물 조건",
        "map_title": "🗺️ 조건에 맞는 빈집 위치 지도",
        "price_title": "💰 예상 가격 비교 차트",
        "table_title": "📋 상세 데이터 테이블",
        "property_title": "🏠 건물 조건 필터",
        "no_data": "조건에 맞는 빈집이 없습니다. 좌측 필터를 다시 설정해보세요.",
        "location": "위치",
        "price": "예상가격",
        "hospital_dist": "병원 거리",
        "school_dist": "학교 거리",
        "industry_dist": "직장 거리",
        "area": "면적",
        "rooms": "방 개수",
        "bathrooms": "욕실 개수",
        "floors": "층수",
        "update_map": "🔄 지도 업데이트",
        "legend_title": "🗺️ 지도 범례",
        "legend_empty": "🏠 빈집",
        "legend_hospital": "🏥 병원",
        "legend_school": "🏫 학교",
        "distance_500": "500m 이내",
        "distance_1000": "1000m 이내",
        "distance_2000": "2000m 이내",
        "distance_5000": "5000m 이내",
        "distance_all": "거리 상관없음",
        "min_area": "최소 면적",
        "max_area": "최대 면적",
        "select_rooms": "방 개수 선택",
        "select_bathrooms": "욕실 개수 선택",
        "select_floors": "층수 선택"
    },
    "English": {
        "title": "🏘️ Empty House Utilization Dashboard",
        "filter_header": "📌 Select Filter Conditions",
        "language": "Language",
        "city_select": "🏙️ Select Region",
        "max_hospital": "🏥 Max Distance to Hospital",
        "max_school": "🏫 Max Distance to School",
        "max_industry": "🏢 Max Distance to Workplace",
        "max_price": "💰 Max Expected Price (10K KRW)",
        "user_type": "👥 User Type",
        "property_conditions": "🏠 Property Conditions",
        "area_filter": "Area Condition (㎡)",
        "room_filter": "Number of Rooms",
        "bathroom_filter": "Number of Bathrooms",
        "floor_filter": "Number of Floors",
        "tab1": "🗺️ Map View",
        "tab2": "💰 Price Comparison",
        "tab3": "📋 Detailed Table",
        "tab4": "🏠 Property Conditions",
        "map_title": "🗺️ Map of Empty Houses Meeting Conditions",
        "price_title": "💰 Expected Price Comparison Chart",
        "table_title": "📋 Detailed Data Table",
        "property_title": "🏠 Property Condition Filters",
        "no_data": "No empty houses match the conditions. Please adjust the filters.",
        "location": "Location",
        "price": "Expected Price",
        "hospital_dist": "Hospital Distance",
        "school_dist": "School Distance", 
        "industry_dist": "Workplace Distance",
        "area": "Area",
        "rooms": "Rooms",
        "bathrooms": "Bathrooms",
        "floors": "Floors",
        "update_map": "🔄 Update Map",
        "legend_title": "🗺️ Map Legend",
        "legend_empty": "🏠 Empty Houses",
        "legend_hospital": "🏥 Hospitals",
        "legend_school": "🏫 Schools",
        "distance_500": "Within 500m",
        "distance_1000": "Within 1000m",
        "distance_2000": "Within 2000m",
        "distance_5000": "Within 5000m",
        "distance_all": "Any Distance",
        "min_area": "Min Area",
        "max_area": "Max Area",
        "select_rooms": "Select Rooms",
        "select_bathrooms": "Select Bathrooms",
        "select_floors": "Select Floors"
    }
}

USER_TYPES = {
    "한국어": {
        "1인형": "1인형 (E9 근로자, 외국인 유학생)",
        "단기거주형": "단기 거주형 (계절근로자, 단기 취업자)",
        "동료형": "동료형 (2-3인 공동 거주)",
        "전체": "전체"
    },
    "English": {
        "1인형": "Single Type (E9 Workers, Foreign Students)",
        "단기거주형": "Short-term Type (Seasonal Workers)",
        "동료형": "Shared Type (2-3 Person Co-living)",
        "전체": "All Types"
    }
}

DISTANCE_OPTIONS = {
    "한국어": {
        500: "500m 이내",
        1000: "1000m 이내", 
        2000: "2000m 이내",
        5000: "5000m 이내",
        10000: "거리 상관없음"
    },
    "English": {
        500: "Within 500m",
        1000: "Within 1000m",
        2000: "Within 2000m", 
        5000: "Within 5000m",
        10000: "Any Distance"
    }
}

# 시도별 중심 좌표 및 경계
CITY_DATA = {
    "한국어": {
        "영주시": {"center": [36.8065, 128.6239], "bounds": {"lat_min": 36.7, "lat_max": 36.9, "lon_min": 128.5, "lon_max": 128.7}},
        "구미시": {"center": [36.1196, 128.3441], "bounds": {"lat_min": 36.0, "lat_max": 36.2, "lon_min": 128.2, "lon_max": 128.5}},
        "포항시": {"center": [36.0190, 129.3435], "bounds": {"lat_min": 35.9, "lat_max": 36.1, "lon_min": 129.2, "lon_max": 129.5}},
        "경주시": {"center": [35.8562, 129.2247], "bounds": {"lat_min": 35.7, "lat_max": 36.0, "lon_min": 129.1, "lon_max": 129.4}},
        "안동시": {"center": [36.5684, 128.7294], "bounds": {"lat_min": 36.4, "lat_max": 36.7, "lon_min": 128.6, "lon_max": 128.9}},
        "김천시": {"center": [36.1396, 128.1133], "bounds": {"lat_min": 36.0, "lat_max": 36.3, "lon_min": 128.0, "lon_max": 128.3}}
    },
    "English": {
        "Yeongju": {"center": [36.8065, 128.6239], "bounds": {"lat_min": 36.7, "lat_max": 36.9, "lon_min": 128.5, "lon_max": 128.7}},
        "Gumi": {"center": [36.1196, 128.3441], "bounds": {"lat_min": 36.0, "lat_max": 36.2, "lon_min": 128.2, "lon_max": 128.5}},
        "Pohang": {"center": [36.0190, 129.3435], "bounds": {"lat_min": 35.9, "lat_max": 36.1, "lon_min": 129.2, "lon_max": 129.5}},
        "Gyeongju": {"center": [35.8562, 129.2247], "bounds": {"lat_min": 35.7, "lat_max": 36.0, "lon_min": 129.1, "lon_max": 129.4}},
        "Andong": {"center": [36.5684, 128.7294], "bounds": {"lat_min": 36.4, "lat_max": 36.7, "lon_min": 128.6, "lon_max": 128.9}},
        "Gimcheon": {"center": [36.1396, 128.1133], "bounds": {"lat_min": 36.0, "lat_max": 36.3, "lon_min": 128.0, "lon_max": 128.3}}
    }
}

@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    
    # 예상가격 계산
    if "예상가격(만원)" not in df.columns:
        df["예상가격(만원)"] = (
            (10000 - df["NEAR_DIST_hospital(m)"]) * 0.01 +
            (10000 - df["NEAR_DIST_school(m)"]) * 0.005 +
            (10000 - df["NEAR_DIST_industry(m)"]) * 0.002
        ).astype(int)
    
    # 데이터 프레임 길이 확인
    data_length = len(df)
    
    # 샘플 데이터가 없는 경우 기본값 추가 (길이 맞춤)
    if "면적(㎡)" not in df.columns:
        import numpy as np
        np.random.seed(42)  # 재현가능한 랜덤값
        df["면적(㎡)"] = np.random.choice([25, 35, 18, 65, 22, 45, 30, 40, 28, 55], size=data_length)
    
    if "방개수" not in df.columns:
        import numpy as np
        np.random.seed(43)
        df["방개수"] = np.random.choice([1, 2, 3, 4], size=data_length, p=[0.4, 0.3, 0.2, 0.1])
    
    if "욕실개수" not in df.columns:
        import numpy as np
        np.random.seed(44)
        df["욕실개수"] = np.random.choice([1, 2, 3], size=data_length, p=[0.6, 0.3, 0.1])
    
    if "층수" not in df.columns:
        import numpy as np
        np.random.seed(45)
        df["층수"] = np.random.choice([1, 2, 3, 4, 5], size=data_length, p=[0.3, 0.25, 0.2, 0.15, 0.1])
    
    if "행정구역" not in df.columns:
        import numpy as np
        np.random.seed(46)
        districts = ["영주시 영주동", "영주시 휴천동", "영주시 가흥동", "영주시 하망동", "영주시 상망동", 
                    "구미시 송정동", "구미시 원평동", "포항시 북구", "포항시 남구", "경주시 황남동",
                    "안동시 명륜동", "김천시 평화동"]
        df["행정구역"] = np.random.choice(districts, size=data_length)
    
    return df

@st.cache_data
def load_hospital_data():
    try:
        hospital_df = pd.read_excel("경북_병원위치.xlsx")
        
        # 컬럼명 확인 및 표준화
        hospital_df.columns = hospital_df.columns.str.strip()
        
        # 필요한 컬럼들을 찾아서 매핑
        name_col = None
        lat_col = None
        lon_col = None
        address_col = None
        
        for col in hospital_df.columns:
            if '병원' in col or '의료' in col or '사업장명' in col:
                name_col = col
            elif '위도' in col:
                lat_col = col
            elif '경도' in col:
                lon_col = col
            elif '주소' in col and '도로명' in col:
                address_col = col
        
        if name_col and lat_col and lon_col:
            result_df = pd.DataFrame({
                'name': hospital_df[name_col],
                'lat': pd.to_numeric(hospital_df[lat_col], errors='coerce'),
                'lon': pd.to_numeric(hospital_df[lon_col], errors='coerce'),
                'address': hospital_df[address_col] if address_col else hospital_df[name_col]
            })
            
            # NaN 값 제거
            result_df = result_df.dropna(subset=['lat', 'lon'])
            return result_df
        
    except Exception as e:
        st.warning(f"병원 데이터 로드 실패: {e}")
    
    # 기본 데이터 반환
    hospital_data = [
        {"name": "자강병원", "lat": 35.84307838, "lon": 129.2066455, "address": "경상북도 경주시 금성로 287"},
        {"name": "구미으뜸병원", "lat": 36.12242557, "lon": 128.3207336, "address": "경상북도 구미시 금오산로 198-20"},
        {"name": "영천요양병원", "lat": 35.98763573, "lon": 128.9246662, "address": "경상북도 영천시 천문로 594-0"},
        {"name": "봄요양병원", "lat": 36.0870495, "lon": 129.3849703, "address": "경상북도 포항시 북구 법원로129번길 12-0"},
        {"name": "구미차병원", "lat": 36.11446604, "lon": 128.3405288, "address": "경상북도 구미시 신시로10길 12"},
        {"name": "로이스제일치과병원", "lat": 36.57326398, "lon": 128.6970862, "address": "경상북도 안동시 노하길 431-0"},
        {"name": "영주성모병원", "lat": 36.8065, "lon": 128.6239, "address": "경상북도 영주시 중앙로 123"},
        {"name": "김천제일병원", "lat": 36.1396, "lon": 128.1133, "address": "경상북도 김천시 대학로 456"}
    ]
    return pd.DataFrame(hospital_data)

@st.cache_data
def load_school_data():
    try:
        school_df = pd.read_excel("경북_학교위치.xlsx")
        
        # 컬럼명 확인 및 표준화
        school_df.columns = school_df.columns.str.strip()
        
        # 필요한 컬럼들을 찾아서 매핑
        name_col = None
        lat_col = None
        lon_col = None
        address_col = None
        
        for col in school_df.columns:
            if '학교명' in col or '학교' in col:
                name_col = col
            elif '위도' in col:
                lat_col = col
            elif '경도' in col:
                lon_col = col
            elif '주소' in col and '도로명' in col:
                address_col = col
        
        if name_col and lat_col and lon_col:
            result_df = pd.DataFrame({
                'name': school_df[name_col],
                'lat': pd.to_numeric(school_df[lat_col], errors='coerce'),
                'lon': pd.to_numeric(school_df[lon_col], errors='coerce'),
                'address': school_df[address_col] if address_col else school_df[name_col]
            })
            
            # NaN 값 제거
            result_df = result_df.dropna(subset=['lat', 'lon'])
            return result_df
        
    except Exception as e:
        st.warning(f"학교 데이터 로드 실패: {e}")
    
    # 기본 데이터 반환
    school_data = [
        {"name": "천부초등학교", "lat": 37.5366566, "lon": 130.8715273, "address": "경상북도 울릉군 북면 천부길 95-3"},
        {"name": "장천초등학교", "lat": 36.13082394, "lon": 128.4944932, "address": "경상북도 구미시 장천면 강동로 236"},
        {"name": "초서초등학교", "lat": 36.09412747, "lon": 129.3333431, "address": "경상북도 포항시 북구 초곡지구로 152"},
        {"name": "포항용산초등학교", "lat": 35.94818, "lon": 129.4085662, "address": "경상북도 포항시 남구 오천읍 정몽주로 309"},
        {"name": "풍양초등학교", "lat": 36.51203002, "lon": 128.299058, "address": "경상북도 예천군 풍양면 낙상1길 50-10"},
        {"name": "영주초등학교", "lat": 36.8065, "lon": 128.6239, "address": "경상북도 영주시 학교로 789"},
        {"name": "김천중학교", "lat": 36.1396, "lon": 128.1133, "address": "경상북도 김천시 교육로 321"}
    ]
    return pd.DataFrame(school_data)

def get_user_type_filter(user_type):
    """사용자 유형에 따른 필터 조건 반환"""
    if user_type == "1인형":
        return {"면적": (14, 26), "방개수": [1]}
    elif user_type == "단기거주형":
        return {"면적": (20, 40), "방개수": [1, 2]}
    elif user_type == "동료형":
        return {"면적": (60, 200), "방개수": [2, 3, 4]}
    else:
        return None

# 메인 앱
def main():
    # 언어 선택
    lang = st.selectbox("🌐 Language / 언어", ["한국어", "English"])
    texts = LANGUAGES[lang]
    
    st.title(texts["title"])
    
    # 데이터 로드
    df = load_data()
    hospital_df = load_hospital_data()
    school_df = load_school_data()
    
    # 사이드바 필터
    st.sidebar.header(texts["filter_header"])
    
    # 지역 선택
    city_options = list(CITY_DATA[lang].keys())
    selected_city = st.sidebar.selectbox(texts["city_select"], city_options)
    
    # 사용자 유형 선택
    user_type_options = USER_TYPES[lang]
    user_type = st.sidebar.selectbox(texts["user_type"], list(user_type_options.values()))
    
    # 선택된 사용자 유형에 따른 키 찾기
    selected_type_key = None
    for key, value in user_type_options.items():
        if value == user_type:
            selected_type_key = key
            break
    
    # 거리 필터 - 기본값을 1000m로 설정
    distance_options = DISTANCE_OPTIONS[lang]
    max_hospital = st.sidebar.selectbox(texts["max_hospital"], 
                                       options=list(distance_options.keys()),
                                       format_func=lambda x: distance_options[x],
                                       index=2)  # 1000m가 기본값
    
    max_school = st.sidebar.selectbox(texts["max_school"],
                                     options=list(distance_options.keys()),
                                     format_func=lambda x: distance_options[x],
                                     index=1)  # 1000m가 기본값
    
    max_industry = st.sidebar.selectbox(texts["max_industry"],
                                       options=list(distance_options.keys()),
                                       format_func=lambda x: distance_options[x],
                                       index=4)  # 1000m가 기본값
    
    # 가격 필터
    max_price = st.sidebar.slider(texts["max_price"], 0, 500, 300)
    
    # 탭 생성 - 4개 탭으로 확장
    tab1, tab2, tab3, tab4 = st.tabs([texts["tab1"], texts["tab2"], texts["tab3"], texts["tab4"]])
    
    # 탭 4에서 사용할 건물 조건 필터 (세션 상태 사용)
    if 'min_area' not in st.session_state:
        st.session_state.min_area = 0
    if 'max_area' not in st.session_state:
        st.session_state.max_area = 200
    if 'selected_rooms' not in st.session_state:
        st.session_state.selected_rooms = [1, 2, 3, 4]
    if 'selected_bathrooms' not in st.session_state:
        st.session_state.selected_bathrooms = [1, 2, 3]
    if 'selected_floors' not in st.session_state:
        st.session_state.selected_floors = [1, 2, 3, 4, 5]
    
    # 필터링 로직을 함수로 분리
    def apply_filters():
        filtered = df[
            (df["NEAR_DIST_hospital(m)"] <= max_hospital) &
            (df["NEAR_DIST_school(m)"] <= max_school) &
            (df["NEAR_DIST_industry(m)"] <= max_industry) &
            (df["예상가격(만원)"] <= max_price)
        ]
        
        # 건물 조건 필터링 (세션 상태에서 가져오기)
        if "면적(㎡)" in df.columns:
            filtered = filtered[
                (filtered["면적(㎡)"] >= st.session_state.min_area) &
                (filtered["면적(㎡)"] <= st.session_state.max_area)
            ]
        
        if "방개수" in df.columns and st.session_state.selected_rooms:
            filtered = filtered[filtered["방개수"].isin(st.session_state.selected_rooms)]
        
        if "욕실개수" in df.columns and st.session_state.selected_bathrooms:
            filtered = filtered[filtered["욕실개수"].isin(st.session_state.selected_bathrooms)]
        
        if "층수" in df.columns and st.session_state.selected_floors:
            filtered = filtered[filtered["층수"].isin(st.session_state.selected_floors)]
        
        # 사용자 유형별 추가 필터링 (선택적)
        user_filter = get_user_type_filter(selected_type_key)
        if user_filter and selected_type_key != "전체":
            if "면적" in user_filter:
                filtered = filtered[
                    (filtered["면적(㎡)"] >= user_filter["면적"][0]) &
                    (filtered["면적(㎡)"] <= user_filter["면적"][1])
                ]
            if "방개수" in user_filter:
                filtered = filtered[filtered["방개수"].isin(user_filter["방개수"])]
        
        return filtered
    
    # 탭 1: 지도
    with tab1:
        st.subheader(texts["map_title"])
        
        # 지도 업데이트 버튼
        col1, col2 = st.columns([3, 1])
        with col2:
            update_map = st.button(texts["update_map"])
        
        # 지도 업데이트 버튼을 눌렀을 때만 필터링 및 지도 생성
        if update_map or 'current_filtered_data' not in st.session_state:
            filtered = apply_filters()
            st.session_state.current_filtered_data = filtered
            
            with col1:
                st.write(f"조건에 맞는 빈집: **{len(filtered)}개**")
            
            if filtered.empty:
                st.warning(texts["no_data"])
                st.session_state.map_data = None
            else:
                # 선택된 도시 중심으로 지도 생성
                city_center = CITY_DATA[lang][selected_city]["center"]
                city_bounds = CITY_DATA[lang][selected_city]["bounds"]
                
                m = folium.Map(location=city_center, zoom_start=13)
                
                # 빈집 마커 추가
                for _, row in filtered.iterrows():
                    popup_text = f"""
                    <b>{texts['location']}:</b> {row['위치']}<br>
                    <b>{texts['price']}:</b> {row['예상가격(만원)']}만원<br>
                    <b>{texts['hospital_dist']}:</b> {int(row['NEAR_DIST_hospital(m)'])}m<br>
                    <b>{texts['school_dist']}:</b> {int(row['NEAR_DIST_school(m)'])}m<br>
                    <b>{texts['industry_dist']}:</b> {int(row['NEAR_DIST_industry(m)'])}m<br>
                    <b>{texts['area']}:</b> {row['면적(㎡)']}㎡<br>
                    <b>{texts['rooms']}:</b> {row['방개수']}개<br>
                    <b>{texts['bathrooms']}:</b> {row['욕실개수']}개<br>
                    <b>{texts['floors']}:</b> {row['층수']}층
                    """
                    
                    folium.Marker(
                        location=[row["Latitude"], row["Longitude"]],
                        popup=folium.Popup(popup_text, max_width=300),
                        icon=folium.Icon(color="green", icon="home", prefix="fa")
                    ).add_to(m)
                
                # 병원 마커 추가 (선택된 도시 주변만 표시)
                for _, hospital in hospital_df.iterrows():
                    if (city_bounds['lat_min'] <= hospital["lat"] <= city_bounds['lat_max'] and
                        city_bounds['lon_min'] <= hospital["lon"] <= city_bounds['lon_max']):
                        folium.Marker(
                            location=[hospital["lat"], hospital["lon"]],
                            popup=folium.Popup(f"🏥 {hospital['name']}<br>{hospital['address']}", max_width=250),
                            icon=folium.Icon(color="red", icon="plus-square", prefix="fa")
                        ).add_to(m)
                
                # 학교 마커 추가 (선택된 도시 주변만 표시)
                for _, school in school_df.iterrows():
                    if (city_bounds['lat_min'] <= school["lat"] <= city_bounds['lat_max'] and
                        city_bounds['lon_min'] <= school["lon"] <= city_bounds['lon_max']):
                        folium.Marker(
                            location=[school["lat"], school["lon"]],
                            popup=folium.Popup(f"🏫 {school['name']}<br>{school['address']}", max_width=250),
                            icon=folium.Icon(color="blue", icon="book", prefix="fa")
                        ).add_to(m)
                st.session_state.map_data = m
        else:
            # 기존 데이터로 표시 (업데이트 버튼을 누르지 않은 경우)
            if 'current_filtered_data' in st.session_state:
                with col1:
                    st.write(f"조건에 맞는 빈집: **{len(st.session_state.current_filtered_data)}개**")
        
        # 지도 표시
        if 'map_data' in st.session_state and st.session_state.map_data is not None:
            st_folium(st.session_state.map_data, width=700, height=500, returned_objects=[])
        
        # 지도 범례를 지도 밖에 표시
        st.markdown("---")
        st.subheader(texts["legend_title"])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(texts["legend_empty"])
        with col2:
            st.markdown(texts["legend_hospital"])  
        with col3:
            st.markdown(texts["legend_school"])
        
    # 탭 2: 가격 비교
    with tab2:
        st.subheader(texts["price_title"])
        
        filtered = apply_filters()
        
        if filtered.empty:
            st.warning(texts["no_data"])
        else:
            import plotly.express as px
            
            # 가격 순으로 정렬
            filtered_sorted = filtered.sort_values('예상가격(만원)', ascending=True)
            
            fig = px.bar(
                filtered_sorted.head(20),  # 상위 20개만 표시
                x='위치',
                y='예상가격(만원)',
                title=texts["price_title"],
                labels={'위치': texts["location"], '예상가격(만원)': texts["price"]}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # 가격 통계
            st.write(f"**평균 가격:** {filtered['예상가격(만원)'].mean():.1f}만원")
            st.write(f"**최저 가격:** {filtered['예상가격(만원)'].min()}만원")
            st.write(f"**최고 가격:** {filtered['예상가격(만원)'].max()}만원")
    
    # 탭 3: 상세 테이블
    with tab3:
        st.subheader(texts["table_title"])
        
        filtered = apply_filters()
        
        if filtered.empty:
            st.warning(texts["no_data"])
        else:
            # 컬럼명 번역
            display_columns = {
                '위치': texts["location"],
                '예상가격(만원)': texts["price"],
                'NEAR_DIST_hospital(m)': texts["hospital_dist"],
                'NEAR_DIST_school(m)': texts["school_dist"],
                'NEAR_DIST_industry(m)': texts["industry_dist"],
                '면적(㎡)': texts["area"],
                '방개수': texts["rooms"],
                '욕실개수': texts["bathrooms"],
                '층수': texts["floors"]
            }
            
            display_df = filtered[list(display_columns.keys())].copy()
            display_df.columns = list(display_columns.values())
            
            st.dataframe(display_df, use_container_width=True)
            
            # CSV 다운로드
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv,
                file_name=f"empty_houses_{selected_city}.csv",
                mime="text/csv"
            )
        # 요약 통계
        st.write("### 📊 Summary Statistics" if lang == "English" else "### 📊 요약 통계")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Properties" if lang == "English" else "총 물건 수", len(filtered))
        with col2:
            st.metric("Avg Price" if lang == "English" else "평균 가격", f"{filtered['예상가격(만원)'].mean():.0f}만원")
        with col3:
            st.metric("Avg Area" if lang == "English" else "평균 면적", f"{filtered['면적(㎡)'].mean():.1f}㎡")
        with col4:
            st.metric("Districts" if lang == "English" else "행정구역 수", filtered['행정구역'].nunique())

    # 탭 4: 건물 조건
    with tab4:
        st.subheader(texts["property_title"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### " + texts["area_filter"])
            min_area = st.number_input(texts["min_area"], min_value=0, max_value=200, value=st.session_state.min_area)
            max_area = st.number_input(texts["max_area"], min_value=0, max_value=200, value=st.session_state.max_area)
            
            st.markdown("#### " + texts["room_filter"])
            selected_rooms = st.multiselect(
                texts["select_rooms"],
                options=[1, 2, 3, 4],
                default=st.session_state.selected_rooms
            )
        
        with col2:
            st.markdown("#### " + texts["bathroom_filter"])
            selected_bathrooms = st.multiselect(
                texts["select_bathrooms"],
                options=[1, 2, 3],
                default=st.session_state.selected_bathrooms
            )
            
            st.markdown("#### " + texts["floor_filter"])
            selected_floors = st.multiselect(
                texts["select_floors"],
                options=[1, 2, 3, 4, 5],
                default=st.session_state.selected_floors
            )
        
        # 조건 적용 버튼
        if st.button("✅ 조건 적용"):
            st.session_state.min_area = min_area
            st.session_state.max_area = max_area
            st.session_state.selected_rooms = selected_rooms
            st.session_state.selected_bathrooms = selected_bathrooms
            st.session_state.selected_floors = selected_floors
            st.success("조건이 적용되었습니다!")
        
        # 현재 조건 표시
        st.markdown("#### 현재 적용된 조건")
        st.write(f"**면적:** {st.session_state.min_area}㎡ ~ {st.session_state.max_area}㎡")
        st.write(f"**방개수:** {st.session_state.selected_rooms}")
        st.write(f"**욕실개수:** {st.session_state.selected_bathrooms}")
        st.write(f"**층수:** {st.session_state.selected_floors}")
        
        # 조건에 맞는 데이터 미리보기
        filtered = apply_filters()
        st.markdown("#### 조건에 맞는 빈집 수")
        st.metric("총 개수", len(filtered))

if __name__ == "__main__":
    main()