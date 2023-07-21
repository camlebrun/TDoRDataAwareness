""" On map page"""
import json
from urllib.request import urlopen
import os 
import data_prep
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
with urlopen(
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
) as response:
    countries = json.load(response)

st.set_page_config(layout="wide", page_title="On Map", page_icon=":rainbow:")


fig_general, fig_suicide = st.columns((2, 4))
st.markdown(
    "<h1 style='text-align: center'>Where are trans people killed or pushed to suicide ?</h1>",
    unsafe_allow_html=True,
)

dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()
suicide_data = dc.suicide_data()
violence_data = dc.violence_data()

st.write(
    "According to scientific literature, the transgender population is 2% around the globe with no difference between countries. To take into consideration the difference in population between countries, a ratio per 100K inhabitants has been made "
)

with st.container():
    col1, col2, col3 = st.columns((25, 50, 25))

WORLD_PATH = "tdor_app/custom.geo.json"
with open(WORLD_PATH) as f:
    geo_world = json.load(f)


found = []
missing = []
countries_geo = []

tmp = tdor_data.set_index("Country")

for country in geo_world["features"]:
    country_name = country["properties"]["name"]

    if country_name in tmp.index:
        found.append(country_name)

        geometry = country["geometry"]

        countries_geo.append(
            {"type": "Feature", "geometry": geometry, "id": country_name}
        )
geo_world_ok = {"type": "FeatureCollection", "features": countries_geo}

tdor_data["ratio"] = tdor_data["ratio"].astype(float)
tdor_data = tdor_data.loc[tdor_data["ratio"] != 0]
year_option = tdor_data["year"].unique().tolist()
year = st.select_slider("**Select year**", year_option)
min_ratio_g = tdor_data["ratio"].min()
max_ratio_g = tdor_data["ratio"].max()
tdor_data = tdor_data[tdor_data["year"] == year]
st.write(
    " This maps represent trans peoples killed  or pushed to suicide in  ",
    year)
fig_general = px.choropleth_mapbox(
    tdor_data,
    geojson=geo_world_ok,
    locations="Country",
    color="ratio",
    color_continuous_scale="reds",
    range_color=(min_ratio_g, max_ratio_g),
    opacity=0.5,
    mapbox_style="carto-darkmatter",
    zoom=0.9,
    center={"lat": 30, "lon": -1},
)
fig_general.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig_general.update_layout(width=1100, height=500)
st.plotly_chart(fig_general, use_container_width=True)


with st.container():
    col1, col2 = st.columns(2, gap="large")
    with col2:
        st.markdown(
            "<h4 style='text-align: center'>Suicides</h4>",
            unsafe_allow_html=True)
        suicide_data["ratio"] = suicide_data["ratio"].astype(float)
        min_ratio_s = suicide_data["ratio"].min()
        max_ratio_s = suicide_data["ratio"].max()
        suicide_data = suicide_data.loc[suicide_data["ratio"] != 0]
        suicide_data = suicide_data[suicide_data["year"] == year]
        st.write(
            " This maps represent trans peoples pushed to suicide in  ",
            year)
        fig_suicide = px.choropleth_mapbox(
            suicide_data,
            geojson=geo_world_ok,
            locations="Country",
            color="ratio",
            range_color=(min_ratio_s, max_ratio_s),
            color_continuous_scale="reds",
            opacity=0.5,
            mapbox_style="carto-darkmatter",
            zoom=0,
            center={"lat": 30, "lon": -1},
        )
        fig_suicide.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig_suicide, use_container_width=True)


with col1:
    st.markdown(
        "<h4 style='text-align: center'>Violences</h4>",
        unsafe_allow_html=True)
    violence_data["ratio"] = violence_data["ratio"].astype(float)
    violence_data["ratio"].where(
        violence_data["ratio"] >= 0.0009, 0, inplace=True)
    violence_data = violence_data[violence_data["year"] == year]
    min_ratio_v = violence_data["ratio"].min()
    max_ratio_v = violence_data["ratio"].max()
    st.write(" This maps represent trans peoples killed  in  ", year)
    fig_violence = px.choropleth_mapbox(
        violence_data,
        geojson=geo_world_ok,
        locations="Country",
        color="ratio",
        color_continuous_scale="reds",
        opacity=0.5,
        range_color=(min_ratio_v, max_ratio_v),
        mapbox_style="carto-darkmatter",
        zoom=0,
        center={"lat": 30, "lon": -1},
    )
    fig_violence.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig_violence, use_container_width=True)