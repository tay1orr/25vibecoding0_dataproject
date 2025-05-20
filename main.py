import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Folium + Streamlit 지도 앱 예제")

# 지도 중심 좌표 설정 (예: 서울시청)
latitude = 37.5665
longitude = 126.9780

# Folium 지도 객체 생성
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# 마커 추가
folium.Marker(
    [latitude, longitude],
    popup="여기가 서울시청입니다!",
    tooltip="서울시청"
).add_to(m)

# streamlit-folium으로 지도 렌더링
st_data = st_folium(m, width=700, height=500)

