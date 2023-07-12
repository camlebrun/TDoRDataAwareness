import datetime
import plotly.express as px
import streamlit as st
import data_prep
st.set_page_config(layout="wide", page_title="Previous years")
import os
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
st.markdown(
    "<h1 style='text-align: center'>Previous years</h1>",
    unsafe_allow_html=True)
st.write("This page allows you to compare the number of deaths recorded in the previous years with the current year and Y-2 with Y-1")
st.write("By current date, we mean the date of the day of the consultation of the page VS the date of the day of the consultation of the page Y-1")




dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()

now = datetime.date.today()
current_date = now.strftime('%Y-%m-%d')
current_year = now.strftime('%Y')
date_minus_one = now - datetime.timedelta(days=365)
date_minus_one_format = date_minus_one.strftime('%Y-%m-%d')
year_minus_one = str(int(current_year) - 1)
date_minus_one_format = date_minus_one.strftime('%Y-%m-%d')
nb_current_year = len(tdor_data[tdor_data['Date'] >= current_year])


date_minus_1_janv = datetime.datetime(int(year_minus_one), 1, 1)
date_minus_1_janv_format = date_minus_1_janv.strftime('%Y-%m-%d')
date_minus_2_janv = datetime.datetime(int(year_minus_one) - 1, 1, 1)
date_minus_2_janv_format = date_minus_2_janv.strftime('%Y-%m-%d')
date_minus_two = date_minus_one - \
    datetime.timedelta(days=365)
date_minus_two_format = date_minus_two.strftime('%Y-%m-%d')

nb_death_y_minus_1 = len(tdor_data[(tdor_data['Date'] >= date_minus_1_janv_format) & (
    tdor_data['Date'] <= date_minus_one_format)])

nb_death_y_minus_2 = len(tdor_data[(tdor_data['Date'] >= date_minus_2_janv_format) & (
    tdor_data['Date'] <= date_minus_two_format)])

delta_y_minus_1 = nb_current_year - nb_death_y_minus_1
delta_y_minus_2 = nb_death_y_minus_1 - nb_death_y_minus_2
with st.container():
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.metric(
            "Number of death in " +
            current_year,
            nb_current_year,
            delta=delta_y_minus_1)
    with col2:
        st.metric("Number of death in " + str(int(year_minus_one)),
                  nb_death_y_minus_1, delta=delta_y_minus_2)
    with col3:
        st.metric("Number of death in " +
                  str(int(year_minus_one) - 1), nb_death_y_minus_2)

fig_annual = px.line(
    tdor_data,
    x="year",
    y="nb_victims_year",
    labels={
        "nb_victims_year": "Number of victims yearly",
        "Year": "Years"}
)
fig_annual.layout.xaxis.fixedrange = True
fig_annual.layout.yaxis.fixedrange = True
fig_annual.update_traces(mode="markers+lines")
fig_annual.update_layout(hovermode="x unified")
fig_annual.update_layout(hoverlabel=dict(font_size=14))
fig_annual.update_traces(hovertemplate="%{y}")
fig_annual.update_layout(width=1100, height=500)
fig_annual.update_traces(textposition='top center')
fig_annual.update_traces(line_color='#FF0000')
fig_annual.update_layout(title="Number of deaths per year")
st.plotly_chart(fig_annual, use_container_width=False)
