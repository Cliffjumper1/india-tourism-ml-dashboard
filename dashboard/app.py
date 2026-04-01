import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Tourism AI Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🇮🇳 India Tourism Analytics Dashboard")

DATA_PATH = "data/processed/cleaned_tourism.csv"

if not os.path.exists(DATA_PATH):
    st.error("Processed data not found. Please upload dataset.")
    st.stop()

df = pd.read_csv(DATA_PATH)

state_col = [col for col in df.columns if 'state' in col][0]

st.sidebar.header("Filters")

states = st.sidebar.multiselect(
    "Select State",
    options=df[state_col].unique(),
    default=df[state_col].unique()[:5]
)

filtered_df = df[df[state_col].isin(states)]

col1, col2, col3 = st.columns(3)

col1.metric("Total Tourists", int(filtered_df['total_tourists'].sum()))
col2.metric("Avg Growth Rate", round(filtered_df['growth_rate'].mean(), 2))
col3.metric("Records", len(filtered_df))


st.subheader("Tourism Trends")

fig = px.line(
    filtered_df,
    x="month_num",
    y="total_tourists",
    color=state_col
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top States")

top_states = (
    filtered_df.groupby(state_col)['total_tourists']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2 = px.bar(
    x=top_states.values,
    y=top_states.index,
    orientation='h'
)

st.plotly_chart(fig2, use_container_width=True)


st.subheader("Compare States")

compare_states = st.multiselect(
    "Select states to compare",
    options=df[state_col].unique(),
    default=df[state_col].unique()[:2]
)

if len(compare_states) >= 2:
    compare_df = df[df[state_col].isin(compare_states)]

    fig_compare = px.line(
        compare_df,
        x="month_num",
        y="total_tourists",
        color=state_col
    )

    st.plotly_chart(fig_compare, use_container_width=True)
else:
    st.warning("Select at least 2 states")


st.subheader("Insights")

top_state = df.groupby(state_col)['total_tourists'].sum().idxmax()
fastest_growth = df.groupby(state_col)['growth_rate'].mean().idxmax()

st.success(f"Top State: {top_state}")
st.info(f"Fastest Growing: {fastest_growth}")

st.subheader("Best State by Month")

month = st.selectbox("Select Month", sorted(df['month_num'].unique()))

best_state = (
    df[df['month_num'] == month]
    .sort_values(by="total_tourists", ascending=False)
    .iloc[0][state_col]
)

st.success(f"Best State in Month {month}: {best_state}")