import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("서울특별시 연령별 남녀 인구 분포 (2025년 4월)")

# CSV 파일 업로드
uploaded_file = st.file_uploader("남녀구분 인구 CSV 파일을 업로드하세요 (cp949 인코딩)", type=["csv"])

if uploaded_file is not None:
    df_gender = pd.read_csv(uploaded_file, encoding='cp949')

    # 서울특별시 전체(코드: 1100000000)만 추출
    seoul_gender_row = df_gender[df_gender['행정구역'].str.contains('서울특별시  \(1100000000\)')]

    # 연령별 남자/여자 컬럼 추출
    male_cols = [col for col in df_gender.columns if '남자' in col and ('세' in col or '이상' in col)]
    female_cols = [col for col in df_gender.columns if '여자' in col and ('세' in col or '이상' in col)]

    male_pop = seoul_gender_row[male_cols].astype(int).values.flatten()
    female_pop = seoul_gender_row[female_cols].astype(int).values.flatten()
    age_labels = [col.split('_')[-1] for col in male_cols]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=age_labels, y=male_pop, name="남자"))
    fig.add_trace(go.Bar(x=age_labels, y=female_pop, name="여자"))

    fig.update_layout(
        xaxis_title="연령",
        yaxis_title="인구수",
        xaxis_tickangle=-45,
        barmode='group'
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("왼쪽에서 파일을 업로드하면 시각화가 나타납니다.")
