import streamlit as st
import pandas as pd
import data_prep
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL")

class MemorialCardSearcher:
    def __init__(self):
        dc = data_prep.DataCollector(URL)
        self.tdor_data = dc.get_data()
        self.tdor_data = self.tdor_data.reset_index(drop=True)
        self.tdor_data = self.tdor_data[['name', 'permalink']]
        self.tdor_data = self.tdor_data.rename(
            columns={
                'name': 'Name',
                'permalink': 'Memory card from TransLivesMatter'
            })

    def search_by_name(self, name_search):
        if name_search:
            selected_options_name = self.tdor_data[self.tdor_data['Name'].str.lower().str.contains(name_search.lower())]
            return selected_options_name
        return pd.DataFrame()

# Configuration de la page Streamlit
st.set_page_config(layout="wide", page_title="Memorial card", page_icon=":rainbow:")
st.markdown("<h1 style='text-align: center'>Search memorial card </h1>", unsafe_allow_html=True)
st.empty()
st.empty()
st.write("This research tool allows you to put names and stories behind the numbers. You can search with criteria or directly with the name of the person ")
st.empty()

searcher = MemorialCardSearcher()

# Recherche par nom
st.markdown("<h5 style='text-align: center'>Search by name</h5>", unsafe_allow_html=True)
name_search = st.text_input("Enter name to search:", value="")

selected_options_name = searcher.search_by_name(name_search)

if not selected_options_name.empty:
    selected_options_name.reset_index(drop=True, inplace=True)
    selected_options_name.index += 1
    st.markdown(selected_options_name.to_html(escape=True, render_links=True), unsafe_allow_html=True)
