import datetime
import pandas as pd
import streamlit as st
import data_prep
import os
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
st.set_page_config(
    layout="wide",
    page_title="Current year",
    page_icon=":rainbow:")


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
categories = ["Violence", "Suicide", "Uncategorised", "Medical", "Custodial"]

N_CATEGORIES = len(categories)
N_COLS = 3
N_ROWS = (N_CATEGORIES - 1) // N_COLS + 1


dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()


prev_years_data = tdor_data[tdor_data['year'] < tdor_data['year'].max()]
now = datetime.date.today()
current_date = now.strftime('%Y-%m-%d')
current_date = datetime.datetime.strptime(current_date, '%Y-%m-%d')
current_year = current_date.year
current_year_data = tdor_data[tdor_data['year'] == current_year]
date_str = current_date.strftime('%A %d %B %Y')
total = current_year_data['name'].count()

st.markdown(
    f"<h2 style='text-align: center;'>Total number of deaths (reported) at {date_str}</h2>",
    unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 50px'>" +
            str(current_year_data['name'].count()) +
            "</h>", unsafe_allow_html=True)

for row in range(N_ROWS):
    with st.container():
        col1, col2, col3 = st.columns(3, gap="small")
        with col1:
            idx = row * N_COLS + 0
            if idx >= N_CATEGORIES:
                break
            category = categories[idx]
            count = tdor_data[tdor_data["year"] ==
                              current_year]["Category"].value_counts().get(category, 0)
            percentage = round(count / total * 100, 1)
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
            count = tdor_data[tdor_data["year"] ==
                              current_year]["Category"].value_counts().get(category, 0)
            percentage = round(count / total * 100, 1)
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
            count = tdor_data[tdor_data["year"] ==
                              current_year]["Category"].value_counts().get(category, 0)
            percentage = round(count / total * 100, 1)
            STR_PER = str(percentage) + "%"
            st.metric(
                label="Number of victims by " +
                category,
                value=count,
                delta=STR_PER)

list_country = current_year_data['Country'].unique().tolist()
st.markdown(
    "<h5 style='text-align: center'>Search by countries</h5>",
    unsafe_allow_html=True)
selected_options_c = st.selectbox("Select one or more options:", list_country)
tdor_data_query = current_year_data[current_year_data['Country']
                                    == selected_options_c]
nb = tdor_data_query["name"].count()
tdor_data_query = tdor_data[tdor_data['Country'] == selected_options_c]
# st.markdown("<h1 style='text-align: center; font-size: 24px'>Total number of deaths for current year</h1>", unsafe_allow_html=True)

st.markdown("### Number of victims by " + str(current_year))
st.metric(label="Total number of victims", value=nb)


for row in range(N_ROWS):
    with st.container():
        col1, col2, col3 = st.columns(N_COLS, gap="small")
        with col1:
            idx = row * N_COLS + 0
            if idx >= N_CATEGORIES:
                break
            category = categories[idx]
            count = tdor_data_query[tdor_data_query["year"] ==
                                    current_year]["Category"].value_counts().get(category, 0)
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
            count = tdor_data_query[tdor_data_query["year"] ==
                                    current_year]["Category"].value_counts().get(category, 0)
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
            count = tdor_data_query[tdor_data_query["year"] ==
                                    current_year]["Category"].value_counts().get(category, 0)
            percentage = round(count / nb * 100, 1)
            STR_PER = str(percentage) + "%"
            st.metric(
                label="Number of victims by " +
                category,
                value=count,
                delta=STR_PER)

            count = tdor_data_query[tdor_data_query["year"] ==
                                    current_year]["Category"].value_counts().get(category, 0)
