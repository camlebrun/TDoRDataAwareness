import datetime
import pandas as pd
import plotly.express as px
import data_prep
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")

class TDORAnalyzer:
    def __init__(self, data):
        self.data = data

    def count_records(self, data, start_date, end_date):
        return len(data[(data['Date'] >= start_date) & (data['Date'] <= end_date)])

    def get_number_of_deaths(self, selected_year):
        selected_data = self.data[self.data['Date'].dt.year == selected_year]
        nb_year_selected = len(selected_data)
        return nb_year_selected

    def calculate_median_deaths_per_month(self, excluded_years):
        other_years_data = self.data[self.data['Date'].dt.year.isin(excluded_years)]
        comptage = other_years_data.groupby(pd.Grouper(key="Date", freq="MS")).size()
        monthly_med = pd.DataFrame(columns=["Month", "Avg"])

        for month in range(1, 13):
            month_name = datetime.datetime(1900, month, 1).strftime('%B')
            avg = round(comptage[comptage.index.month == month].median(), 0)
            monthly_med = pd.concat([monthly_med, pd.DataFrame({"Month": [month_name], "Avg": [avg]})], ignore_index=True)

        return monthly_med

class TDORVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_deaths_per_month(self, selected_year):
        comptage = self.data.groupby(pd.Grouper(key="Date", freq="MS"))\
            .apply(lambda x: (x['Date'].dt.year == selected_year).sum())

        nb_year_selected = len(self.data[self.data['Date'].dt.year == selected_year])
        st.metric("Number of death in " + str(selected_year), nb_year_selected)

        comptage.index = comptage.index.strftime('%B')
        graph_month = px.bar(comptage, x=comptage.index, y=comptage.values)
        graph_month.update_xaxes(title="Month")
        graph_month.update_yaxes(title="Number of reports")
        graph_month.update_traces(text=comptage.values, textposition='inside')
        graph_month.update_traces(
            hovertemplate="Month: %{x}<br>Number of reports: %{y}")
        st.plotly_chart(graph_month, use_container_width=True)

    def plot_median_deaths_per_month(self, excluded_years):
        analyzer = TDORAnalyzer(self.data)
        monthly_med = analyzer.calculate_median_deaths_per_month(excluded_years)
        fig = px.bar(monthly_med, x="Month", y="Avg")
        annual_med = round(monthly_med['Avg'].median())

        fig.add_hline(y=annual_med, line_color="red", line_width=2, line_dash="dot",
                      name=f"Annual Median: {annual_med:.0f}",
                      annotation_text=f"<b>Annual Median: {annual_med:.0f}</b>",
                      annotation_font=dict(size=14))
        fig.update_layout(
            title=f"Number of Transgender Day of Remembrance Deaths per Month ({excluded_years[0]}-{datetime.datetime.now().year-1})",
            xaxis_title="Month",
            yaxis_title="Number of Deaths",
            annotations=[
                dict(
                    x=0.5,
                    y=1.0,
                    showarrow=False,
                    text=f"<b>Monthly median: {annual_med:.0f}</b>",
                    xref="paper",
                    yref="paper",
                    align="center",
                    font=dict(size=14))])
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_xaxes(title="Month")
        fig.update_yaxes(title="median of deaths per month")
        fig.update_layout(title=f"TDOR deaths per month (excluding {datetime.datetime.now().year})")
        st.plotly_chart(fig, use_container_width=True)

# Chargement des données
dc = data_prep.DataCollector(URL)
tdor_data_new = dc.get_data()

# Analyse et visualisation
st.set_page_config(layout="wide", page_title="Months trend")
st.markdown("<h1 style='text-align: center'>Months trend</h1>", unsafe_allow_html=True)

analyzer = TDORAnalyzer(tdor_data_new)
visualizer = TDORVisualizer(tdor_data_new)

list_year = tdor_data_new['Date'].dt.year.unique().tolist()
selected_options = st.selectbox("Select one", list_year, index=len(list_year)-1)

visualizer.plot_deaths_per_month(selected_options)

current_year = datetime.datetime.now().year
other_years = [year for year in list_year if year != current_year]

visualizer.plot_median_deaths_per_month(other_years)
