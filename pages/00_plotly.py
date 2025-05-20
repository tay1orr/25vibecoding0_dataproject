import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("서울특별시 연령별 남녀 인구 분포 (2025년 4월)")

# 깃허브 raw 파일 경로 입력
male_female_url = st.text_input(
    "남녀구분 인구 CSV 파일의 깃허브 raw URL을 입력하세요.",
    value="https://github.com/tay1orr/25vibecoding0_dataproject/blob/main/202504_202504_%EC%97%B0%EB%A0%B9%EB%B3%84%EC%9D%B8%EA%B5%AC%ED%98%84%ED%99%A9_%EC%9B%94%EA%B0%84_%EB%82%A8%EB%85%80%EA%B5%AC%EB%B6%84.csv"
)
sum_url = st.text_input(
    "남녀합계 인구 CSV 파일의 깃허브 raw URL을 입력하세요.",
    value="https://github.com/tay1orr/25vibecoding0_dataproject/blob/main/202504_202504_%EC%97%B0%EB%A0%B9%EB%B3%84%EC%9D%B8%EA%B5%AC%ED%98%84%ED%99%A9_%EC%9B%94%EA%B0%84_%EB%82%A8%EB%85%80%ED%95%A9%EA%B3%84.csv"
)

tab1, tab2 = st.tabs(["남녀구분", "남녀합계"])

with tab1:
    if male_female_url and male_female_url.startswith("http"):
        try:
            df_gender = pd.read_csv(male_female_url, encoding='cp949')
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
        except Exception as e:
            st.error(f"파일을 불러오거나 시각화하는데 문제가 있습니다.\n{e}")
    else:
        st.info("남녀구분 CSV 파일의 raw 깃허브 URL을 입력하면 시각화가 나타납니다.")

with tab2:
    if sum_url and sum_url.startswith("http"):
        try:
            df_sum = pd.read_csv(sum_url, encoding='cp949')
            seoul_row = df_sum[df_sum['행정구역'].str.contains('서울특별시  \(1100000000\)')].iloc[0]
            ages = [col for col in df_sum.columns if '계_' in col and ('세' in col or '이상' in col)]
            populations = seoul_row[ages].astype(int).values
            age_labels = [col.split('_')[-1] for col in ages]
            fig = go.Figure([go.Bar(x=age_labels, y=populations)])
            fig.update_layout(
                title="서울특별시 연령별 인구 분포 (남녀합계)",
                xaxis_title="연령",
                yaxis_title="인구수",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"파일을 불러오거나 시각화하는데 문제가 있습니다.\n{e}")
    else:
        st.info("남녀합계 CSV 파일의 raw 깃허브 URL을 입력하면 시각화가 나타납니다.")
