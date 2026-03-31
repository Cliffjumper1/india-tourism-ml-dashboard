import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.predict import predict_future


st.set_page_config(page_title="Tourism Dashboard", layout="wide")

st.title("🇮🇳 India Tourism Analytics Dashboard")

df = pd.read_csv("data/processed/cleaned_tourism.csv")

st.sidebar.header("Filters")

state_col = [col for col in df.columns if 'state' in col][0]

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
    color=state_col,
    title="Tourists Over Months"
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
    orientation='h',
    title="Top States by Tourism"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Future Predictions")

months = st.slider("Select months", 1, 24, 12)

future = predict_future(months)

fig3 = px.line(
    future,
    x="month_num",
    y="predicted_tourists",
    title="Future Tourism Forecast"
)

st.plotly_chart(fig3, use_container_width=True)

st.dataframe(future)
st.subheader("Compare States")

compare_states = st.multiselect(
    "Select states to compare",
    options=df[state_col].unique(),
    default=df[state_col].unique()[:2]
)

if len(compare_states) > 0:
    compare_df = df[df[state_col].isin(compare_states)]

    fig_compare = px.line(
        compare_df,
        x="month_num",
        y="total_tourists",
        color=state_col,
        title="State Comparison Over Time"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

    st.subheader("Growth Rate Comparison")

    fig_growth = px.line(
        compare_df,
        x="month_num",
        y="growth_rate",
        color=state_col,
        title="Growth Rate Comparison"
    )

    st.plotly_chart(fig_growth, use_container_width=True)

    st.subheader("Best State to Visit")

selected_month = st.selectbox(
    "Select Month",
    sorted(df['month_num'].unique())
)

month_df = df[df['month_num'] == selected_month]

best_state = month_df.sort_values(
    by="total_tourists",
    ascending=False
).iloc[0][state_col]

st.success(f"Best State in Month {selected_month}: {best_state}")

st.subheader("Smart Insights")

top_state = df.groupby(state_col)['total_tourists'].sum().idxmax()
top_value = df.groupby(state_col)['total_tourists'].sum().max()

fastest_growth = df.groupby(state_col)['growth_rate'].mean().idxmax()

col1, col2 = st.columns(2)

col1.success(f"Top Tourism State: {top_state} ({int(top_value)})")
col2.info(f"Fastest Growing State: {fastest_growth}")