import datetime
import plotly.express as px
import streamlit as st
import data_prep
import os
from dotenv import load_dotenv

class DateCalculator:
    def __init__(self):
        now = datetime.date.today()
        self.current_date = now.strftime('%Y-%m-%d')
        self.current_year = now.strftime('%Y')
        self.date_minus_one = now - datetime.timedelta(days=365)
        self.date_minus_one_format = self.date_minus_one.strftime('%Y-%m-%d')
        self.year_minus_one = str(int(self.current_year) - 1)
        self.date_minus_two = self.date_minus_one - datetime.timedelta(days=365)
        self.date_minus_two_format = self.date_minus_two.strftime('%Y-%m-%d')
        self.date_minus_1_janv = datetime.datetime(int(self.year_minus_one), 1, 1)
        self.date_minus_1_janv_format = self.date_minus_1_janv.strftime('%Y-%m-%d')
        self.date_minus_2_janv = datetime.datetime(int(self.year_minus_one) - 1, 1, 1)
        self.date_minus_2_janv_format = self.date_minus_2_janv.strftime('%Y-%m-%d')

    def count_records(self, data, start_date, end_date):
        return len(data[(data['Date'] >= start_date) & (data['Date'] <= end_date)])

    def get_nb_current_year(self, tdor_data):
        return self.count_records(tdor_data, self.current_year, self.current_date)

    def get_nb_death_y_minus_1(self, tdor_data):
        return self.count_records(tdor_data, self.date_minus_1_janv_format, self.date_minus_one_format)

    def get_nb_death_y_minus_2(self, tdor_data):
        return self.count_records(tdor_data, self.date_minus_2_janv_format, self.date_minus_two_format)

    def calculate_delta_y_minus_1(self, tdor_data):
        nb_current_year = self.get_nb_current_year(tdor_data)
        nb_death_y_minus_1 = self.get_nb_death_y_minus_1(tdor_data)
        return nb_current_year - nb_death_y_minus_1

class DataVisualizer:
    def __init__(self, tdor_data):
        self.tdor_data = tdor_data

    def visualize_annual_deaths(self):
        fig_annual = px.line(
            self.tdor_data,
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
        return fig_annual

st.set_page_config(layout="wide", page_title="Previous years")
load_dotenv()
URL = os.getenv("URL")
st.markdown(
    "<h1 style='text-align: center'>Previous years</h1>",
    unsafe_allow_html=True)
st.write("This page allows you to compare the number of deaths recorded in the previous years with the current year and Y-2 with Y-1")
st.write("By current date, we mean the date of the day of the consultation of the page VS the date of the day of the consultation of the page Y-1")

dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()

date_calculator = DateCalculator()

nb_current_year = date_calculator.get_nb_current_year(tdor_data)
nb_death_y_minus_1 = date_calculator.get_nb_death_y_minus_1(tdor_data)
nb_death_y_minus_2 = date_calculator.get_nb_death_y_minus_2(tdor_data)
delta_y_minus_1 = date_calculator.calculate_delta_y_minus_1(tdor_data)
delta_y_minus_2 = nb_death_y_minus_1 - nb_death_y_minus_2

with st.container():
    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        st.metric(
            "Number of death in " + date_calculator.current_year,
            nb_current_year,
            delta=delta_y_minus_1)
    with col2:
        st.metric("Number of death in " + str(int(date_calculator.year_minus_one)),
                  nb_death_y_minus_1, delta=delta_y_minus_2)
    with col3:
        st.metric("Number of death in " +
                  str(int(date_calculator.year_minus_one) - 1), nb_death_y_minus_2)

data_visualizer = DataVisualizer(tdor_data)
fig_annual = data_visualizer.visualize_annual_deaths()
st.plotly_chart(fig_annual, use_container_width=False)
