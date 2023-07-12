import datetime
import pandas as pd
import plotly.express as px
import data_prep
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")

st.set_page_config(layout="wide", page_title="Months trend")

st.markdown(
    "<h1 style='text-align: center'>Months trend</h1>",
    unsafe_allow_html=True)


dc = data_prep.DataCollector(URL)
tdor_data_new = dc.get_data()

list_year = tdor_data_new['Date'].dt.year.unique().tolist()
last_year = max(list_year)
selected_options = st.selectbox(
    "Select one", list_year)

comptage = tdor_data_new.groupby(pd.Grouper(key="Date", freq="MS"))\
    .apply(lambda x: (x['Date'].dt.year == selected_options).sum())
nb_year_selected = len(
    tdor_data_new[tdor_data_new['Date'].dt.year == selected_options])
st.metric("Number of death in " + str(selected_options), nb_year_selected)
view_month = tdor_data_new[tdor_data_new['Date'].dt.year == selected_options]
comptage.index = comptage.index.strftime('%B')
graph_month = px.bar(comptage, x=comptage.index, y=comptage.values)
graph_month.update_xaxes(title="Month")
graph_month.update_yaxes(title="Number of reports")
graph_month.update_traces(text=comptage.values, textposition='inside')
graph_month.update_traces(
    hovertemplate="Month: %{x}<br>Number of reports: %{y}")
st.plotly_chart(graph_month, use_container_width=True)
st.title("Median number of deaths per month")
st.info("We calculate the median number of deaths per month, in oder to see if there is a trend in the number of deaths per month.  \n The median is the middle value of a dataset, and it is often more relevant than the mean when dealing with skewed data or outliers that can significantly affect the mean value.  \n  During the 2000s, there is an obvious lack of data that strongly affects the average and hinders the analysis of the data. There is a significant gap between the values .")
st.write("icon" "", "The median number of deaths per month is calculated by taking the median of the number of deaths per month for all years except the selected year.")
st.write("The red line represents the annual median number of deaths per month.")

current_year = datetime.datetime.now().year
all_years = tdor_data_new['Date'].dt.year.unique().tolist()
other_years = [year for year in all_years if year != current_year]

comptage = tdor_data_new[tdor_data_new['Date'].dt.year.isin(other_years)] \
    .groupby(pd.Grouper(key="Date", freq="MS")) \
    .size()
monthly_med = pd.DataFrame(columns=["Month", "Avg"])
for month in range(1, 13):
    month_name = datetime.datetime(1900, month, 1).strftime('%B')
    avg = round(comptage[comptage.index.month == month].median(), 0)
    monthly_med = pd.concat([monthly_med, pd.DataFrame(
        {"Month": [month_name], "Avg": [avg]})], ignore_index=True)


fig = px.bar(monthly_med, x="Month", y="Avg")
annual_med = round(monthly_med['Avg'].median())

fig.add_hline(y=annual_med, line_color="red", line_width=2, line_dash="dot",
              name=f"Annual Median: {annual_med:.0f}",
              annotation_text=f"<b>Annual Median: {annual_med:.0f}</b>",
              annotation_font=dict(size=14))
fig.update_layout(
    title=f"Number of Transgender Day of Remembrance Deaths per Month \
        ({other_years[0]}-{current_year-1})",
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
            font=dict(
                size=14))])
fig.update_traces(texttemplate='%{y}', textposition='outside')
fig.update_xaxes(title="Month")
fig.update_yaxes(title="median  of deaths per month")
fig.update_layout(title=f"TDOR deaths per month (excluding {current_year})")
st.plotly_chart(fig, use_container_width=True)
