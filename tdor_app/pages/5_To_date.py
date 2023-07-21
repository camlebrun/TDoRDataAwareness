import datetime
import pandas as pd
import streamlit as st
import data_prep
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")


class TDORApp:
    def __init__(self):
        self.dc = data_prep.DataCollector(URL)
        self.tdor_data = self.dc.get_data()
        self.prev_years_data = self.tdor_data[self.tdor_data['year'] < self.tdor_data['year'].max()]
        now = datetime.date.today()
        self.current_date = now.strftime('%Y-%m-%d')
        self.current_date = datetime.datetime.strptime(self.current_date, '%Y-%m-%d')
        self.current_year = self.current_date.year
        self.current_year_data = self.tdor_data[self.tdor_data['year'] == self.current_year]
        self.date_str = self.current_date.strftime('%A %d %B %Y')
        self.total = self.current_year_data['name'].count()

    def display_total_deaths(self):
        st.markdown(
            f"<h2 style='text-align: center;'>Total number of deaths (reported) at {self.date_str}</h2>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h2 style='text-align: center; font-size: 50px'>" + str(self.current_year_data['name'].count()) + "</h>",
            unsafe_allow_html=True
        )

    def display_metrics_by_category(self):
        categories = ["Violence", "Suicide", "Uncategorised", "Medical", "Custodial"]
        N_CATEGORIES = len(categories)
        N_COLS = 3
        N_ROWS = (N_CATEGORIES - 1) // N_COLS + 1

        for row in range(N_ROWS):
            cols = st.columns(N_COLS)
            for i, col in enumerate(cols):
                idx = row * N_COLS + i
                if idx < N_CATEGORIES:
                    category = categories[idx]
                    count = self.current_year_data["Category"].value_counts().get(category, 0)
                    percentage = round(count / self.total * 100, 1)
                    STR_PER = str(percentage) + "%"
                    col.metric(
                        label="Number of victims by " + category,
                        value=count,
                        delta=STR_PER
                    )

    def run(self):
        st.set_page_config(
            layout="wide",
            page_title="Current year",
            page_icon=":rainbow:"
        )

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

        self.display_total_deaths()
        self.display_metrics_by_category()


app = TDORApp()
app.run()
