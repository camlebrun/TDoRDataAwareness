import pandas as pd
import streamlit as st
import data_prep
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")

class TDORSearcher:
    def __init__(self):
        self.tdor_data = self.load_data()

    def load_data(self):
        dc = data_prep.DataCollector(URL)
        tdor_data = dc.get_data()
        tdor_data.reset_index(drop=True)
        tdor_data['Date'] = pd.to_datetime(tdor_data["Date"])
        tdor_data = tdor_data[['Country', 'name', 'age', 'Date', 'Category', 'Cause_of_death']]
        tdor_data["age"] = tdor_data["age"].astype(str)
        tdor_data["age"] = tdor_data["age"].replace("", "Unknown")
        return tdor_data

    def search_data(self, selected_options, selected_options_c, selected_options_cat, name_search):
        selected_options_name = [n for n in self.tdor_data['name'].unique() if name_search.lower() in n.lower()]

        df2 = self.tdor_data[
            (self.tdor_data['Date'].dt.year.isin(selected_options)) &
            (self.tdor_data['Country'].isin(selected_options_c)) &
            (self.tdor_data['Category'].isin(selected_options_cat)) &
            (self.tdor_data['name'].isin(selected_options_name))
        ]

        df2['Date'] = df2['Date'].dt.strftime('%d/%m/%Y')
        df2 = df2.reset_index(drop=True)
        df2.index += 1

        return df2

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="Search")
st.markdown("<h1 style='text-align: center'>Let's not forget them </h1>", unsafe_allow_html=True)
st.empty()
st.write("This research tool allows you to put names and stories behind the numbers. You can search with criteria or directly with the name of the person ")
st.empty()

# Recherche des données
searcher = TDORSearcher()

# Sélection des options
list_year = searcher.tdor_data['Date'].dt.year.unique().tolist()
list_country = searcher.tdor_data['Country'].unique().tolist()
list_Category = searcher.tdor_data['Category'].unique().tolist()
list_name = searcher.tdor_data['name'].unique().tolist()

with st.container():
    col1, col2, col3, col4 = st.columns((25, 25, 25, 25))

    with col1:
        st.markdown("<h5 style='text-align: center'>Search by years</h5>", unsafe_allow_html=True)
        container = st.container()
        selected_options = container.multiselect("Select one or more options:", list_year, [max(list_year)])
        ALL_C_0 = st.checkbox("Select all years")
        if ALL_C_0 and len(selected_options) == 0:
            selected_options = list_year
        elif ALL_C_0 and len(selected_options) > 0:
            ALL_C_0 = False
            st.warning("When searching for a specific year(s) please uncheck the select all box ")

    with col2:
        st.markdown("<h5 style='text-align: center'>Search by countries</h5>", unsafe_allow_html=True)
        selected_options_c = st.multiselect("Select one or more options:", list_country, [])
        ALL_C = st.checkbox("Select all countries", value=True)
        if ALL_C and len(selected_options_c) == 0:
            selected_options_c = list_country
        elif ALL_C and len(selected_options_c) > 0:
            ALL_C = False
            st.warning("When searching for a specific country or countries please uncheck the select all box")

    with col3:
        st.markdown("<h5 style='text-align: center'>Search by category</h5>", unsafe_allow_html=True)
        selected_options_cat = st.multiselect("Select one or more options:", list_Category, [])
        ALL_CO = st.checkbox("Select all category", value=True)
        if ALL_CO and len(selected_options_cat) == 0:
            selected_options_cat = list_Category
        elif ALL_CO and len(selected_options_cat) > 0:
            ALL_CO = False
            st.warning("When searching for a specific category or categories please uncheck the select all box")

    with col4:
        st.markdown("<h5 style='text-align: center'>Search by name</h5>", unsafe_allow_html=True)
        selected_options_name = list_name
        name_search = st.text_input("Enter name to search:", value="")
        if name_search:
            selected_options_name = [n for n in list_name if name_search.lower() in n.lower()]

# Recherche des données en fonction des critères sélectionnés
df2 = searcher.search_data(selected_options, selected_options_c, selected_options_cat, name_search)

# Affichage du résultat
df2 = df2.reset_index(drop=True)
nb = len(df2)
st.metric('Number of victims: ', nb)
st.table(df2)
