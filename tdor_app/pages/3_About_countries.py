
import streamlit as st
import plotly.express as px
import pandas as pd
import data_prep
import os
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
st.set_page_config(
    layout="wide",
    page_title="About countries",
    page_icon=":rainbow:")


dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()

categories = ["Violence", "Suicide", "Uncategorised", "Medical", "Custodial"]

N_CATEGORIES = len(categories)
N_COLS = 4
N_ROWS = (N_CATEGORIES - 1) // N_COLS + 1

st.write(
    """
    <style>
    [data-testid="stMetricDelta"] svg {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


list_country = tdor_data['Country'].unique().tolist()
st.markdown(
    "<h1 style='text-align: center'>Search by countries</h1>",
    unsafe_allow_html=True)
selected_country = st.selectbox("Select one country:", list_country)
tdor_data_query = tdor_data[tdor_data['Country'] == selected_country]
nb = tdor_data_query["name"].count()
st.markdown("### Number of victims for " + selected_country)

st.metric(label="Total number of victims", value=nb)


for row in range(N_ROWS):
    with st.container():
        col1, col2, col3, col4 = st.columns(N_COLS, gap="small")
        with col1:
            idx = row * N_COLS + 0
            if idx >= N_CATEGORIES:
                break
            category = categories[idx]
            count = tdor_data_query[tdor_data_query["Category"]
                                    == category].shape[0]
            percentage = round(count / nb * 100, 1)
            STR_PER = str(percentage) + "%"
            st.metric(
                label="Number of victims by " +
                category,
                value=count,
                delta=STR_PER)

        with col2:
            idx = row * N_COLS + 1
            if idx >= N_CATEGORIES:
                break
            category = categories[idx]
            count = tdor_data_query[tdor_data_query["Category"]
                                    == category].shape[0]
            percentage = round(count / nb * 100, 1)
            STR_PER = str(percentage) + "%"
            st.metric(
                label="Number of victims by " +
                category,
                value=count,
                delta=STR_PER)

        with col3:
            idx = row * N_COLS + 2
            if idx >= N_CATEGORIES:
                break
            category = categories[idx]
            count = tdor_data_query[tdor_data_query["Category"]
                                    == category].shape[0]
            percentage = round(count / nb * 100, 1)
            STR_PER = str(percentage) + "%"
            st.metric(
                label="Number of victims by " +
                category,
                value=count,
                delta=STR_PER)
        with col4:
            idx = row * N_COLS + 3
            if idx >= N_CATEGORIES:
                break
            category = categories[idx]
            count = tdor_data_query[tdor_data_query["Category"]
                                    == category].shape[0]
            percentage = round(count / nb * 100, 1)
            STR_PER = str(percentage) + "%"
            st.metric(
                label="Number of victims by " +
                category,
                value=count,
                delta=STR_PER)

st.write("### Number of victims yearly for " + selected_country)
tdor_data_query = tdor_data_query.groupby(
    ['year']).size().reset_index(name='nb')

fig = px.bar(
    tdor_data_query,
    x="year",
    y="nb",
    text=tdor_data_query['nb'],
    labels={"nb": "Number of victims",
            "year": "Years"},
    width=1000,
    height=600)
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_layout(uniformtext_minsize=15, uniformtext_mode='hide',
                  xaxis={'tickangle': 45, 'dtick': 2},
                  yaxis={'title': 'Number of victims yearly'})
st.plotly_chart(fig, use_container_width=True)


tdor_data_filtered = tdor_data[(tdor_data['Country'] == selected_country)]

tdor_data_query_1 = tdor_data_filtered.groupby(['year', 'Category'])[
    'nb_victims_category_country_year'].count().reset_index()

tdor_data_query_1_yearly = tdor_data_query_1.groupby(
    'year')['nb_victims_category_country_year'].sum().reset_index()
tdor_data_query_1_yearly.rename(
    columns={
        "nb_victims_category_country_year": "nb_yearly"},
    inplace=True)
tdor_data_query_1 = tdor_data_query_1.merge(
    tdor_data_query_1_yearly, on='year')

tdor_data_query_1["percentage_category"] = round(
    tdor_data_query_1["nb_victims_category_country_year"] /
    tdor_data_query_1["nb_yearly"] *
    100,
    1)

st.markdown(
    "### Number of victims by category and percentage for " +
    selected_country)
fig_categorie_exepted_current = px.bar(
    tdor_data_query_1,
    x="year",
    y="nb_victims_category_country_year",
    text=tdor_data_query_1["percentage_category"],
    color='Category',
    custom_data=['Category'],
    labels={
        "nb_victims_category_country_year": "Number of deaths",
        "year": "Years"
    })

fig_categorie_exepted_current.update_traces(
    texttemplate='%{y}',
    hovertemplate='Category: %{customdata[0]}<br>' +
    'Percentage: %{text}%<br>' +
    'Number of Victims: %{y}<br>' +
    '<extra></extra>'
)


fig_categorie_exepted_current.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="auto",
        x=0.5
    )
)
fig_categorie_exepted_current.layout.xaxis.fixedrange = True
fig_categorie_exepted_current.layout.yaxis.fixedrange = True
fig_categorie_exepted_current.update_layout(width=1000, height=500)
fig_categorie_exepted_current.update_layout(hovermode="x unified")
fig_categorie_exepted_current.update_layout(
    xaxis={'tickangle': 45, 'dtick': 2})

st.plotly_chart(
    fig_categorie_exepted_current,
    use_container_width=True)
with st.expander("Show percentage of victims by country"):
    tdor_data_grouped = pd.pivot_table(
        tdor_data,
        values='total',
        index=['Country'],
        aggfunc='count')
    tdor_data_grouped["Percentage"] = (
        tdor_data_grouped["total"] /
        len(tdor_data) *
        100).round(1)
    tdor_data_grouped = tdor_data_grouped[tdor_data_grouped["Percentage"] > 0].sort_values(
        by="Percentage", ascending=False)
    tdor_data_grouped["Percentage"] = tdor_data_grouped["Percentage"].apply(
        lambda x: "{:.1f}%".format(x))
    tdor_data_grouped = tdor_data_grouped.drop(columns="total")
    st.table(tdor_data_grouped.style.set_precision(1))
