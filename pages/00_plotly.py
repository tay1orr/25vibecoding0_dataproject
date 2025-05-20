import streamlit as st
import pandas as pd
import plotly.graph_objects as go

male_female_url = "https://github.com/tay1orr/25vibecoding0_dataproject/blob/main/202504_202504_222.csv"
sum_url = "https://github.com/tay1orr/25vibecoding0_dataproject/blob/main/202504_202504_111.csv"

st.title("서울특별시 연령별 남녀 인구 분포 (2025년 4월)")

tab1, tab2 = st.tabs(["남녀구분", "남녀합계"])

def read_csv_flexible(url):
    try:
        return pd.read_csv(url, encoding='cp949')
    except UnicodeDecodeError:
        return pd.read_csv(url, encoding='utf-8')

with tab1:
    try:
        df_gender = read_csv_flexible(male_female_url)
        seoul_gender_row = df_gender[df_gender['행정구역'].str.contains('서울특별시  \(1100000000\)')]
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

with tab2:
    try:
        df_sum = read_csv_flexible(sum_url)
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
