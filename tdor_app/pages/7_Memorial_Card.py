import streamlit as st
import pandas as pd
import data_prep
import os
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
st.set_page_config(
    layout="wide",
    page_title="Memorial card",
    page_icon=":rainbow:")

st.markdown(
    "<h1 style='text-align: center'>Search memorial card </h1>",
    unsafe_allow_html=True)
st.empty()
st.empty()
st.write("This research tool allows you to put names and stories behind the numbers. You can search with criteria or directly with the name of the person ")
st.empty()


dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()
tdor_data = tdor_data.reset_index(drop=True)
tdor_data = tdor_data[['name', 'permalink']]
tdor_data = tdor_data.rename(
    columns={
        'name': 'Name',
        'permalink': 'Memory card from TransLivesMatter'})


st.markdown(
    "<h5 style='text-align: center'>Search by name</h5>",
    unsafe_allow_html=True)

selected_options_name = pd.DataFrame()
name_search = st.text_input("Enter name to search:", value="")


if name_search:
    selected_options_name = tdor_data[tdor_data['Name'].str.lower(
    ).str.contains(name_search.lower())]

if not selected_options_name.empty:
    selected_options_name.reset_index(drop=True, inplace=True)
    selected_options_name.index += 1
    st.markdown(
        selected_options_name.to_html(
            escape=True,
            render_links=True),
        unsafe_allow_html=True)
