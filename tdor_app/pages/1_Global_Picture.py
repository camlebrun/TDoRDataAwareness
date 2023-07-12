import datetime
import os
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv("URL")
import data_prep
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide", page_title="Global Picture")

fig_annual, fig_categorie_y = st.columns((2, 4))

st.markdown(
    "<h1 style='text-align: center'>The Impact of Transphobia: \
        High Rates of Suicide and Homicide among Transgender peoples</h1>",
    unsafe_allow_html=True,
)
st.write(
    "The transgender community faces significant discrimination, violence, and marginalization, with studies showing higher rates of suicide and homicide among transgender individuals who are victims of transphobia compared to cisgender individuals. This is often a result of societal prejudice and discrimination, as well as lack of legal protections and access to resources. To address these issues, society must increase awareness and understanding of transgender issues, promote acceptance and tolerance, and implement policies to protect the rights and safety of transgender individuals.  The estimated global prevalence of transgender individuals is 2%, but this can vary depending on the study or population and may not accurately reflect the diversity within the community. The understanding and acceptance of transgender individuals also varies across cultures and societies, impacting the prevalence of self-identified transgender individuals. However, it's important to note that the data on transgender individuals is often provided by family members or activists and is likely to be understated."
)

dc = data_prep.DataCollector(URL)
tdor_data = dc.get_data()
prev_years_data = tdor_data[tdor_data["year"] < tdor_data["year"].max()]
now = datetime.date.today()
current_date = now.strftime("%Y-%m-%d")
current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d")
current_year = current_date.year
tdor_date = f"{current_year}-11-20"
tdor_display = datetime.datetime.strptime(tdor_date, "%Y-%m-%d")
totat_victims = tdor_data["name"].count()
with st.container():
    col1, col2, = st.columns(2, gap="small")
    with col1:
        st.markdown("### Total number of victims since 1999")
        st.metric(label="", value=totat_victims)
    with col2:
        mean_age = round(tdor_data["age_cal"].mean())
        mean_age_str = f"{mean_age} years"
        st.markdown("### Average age of victims")
        st.metric(label="", value=mean_age_str)
st.warning('We will not analyze the data by age in the rest of the study due lack of data.', icon="⚠️")

with st.container():
    col1, col2, col3 = st.columns((50, 500, 100))
    with col2:
        if current_date < tdor_display:
            fig_annual = px.line(
                prev_years_data,
                x="year",
                y="nb_victims_year",
                labels={"nb_victims_year": "Number of victims yearly",
                        "year": "Years"},
            )
            fig_annual.update_traces(mode="markers+lines")
            fig_annual.update_layout(hovermode="x unified")
            fig_annual.update_layout(hoverlabel={"font_size": 14})

            fig_annual.update_traces(line_color="#040801")
            fig_annual.update_traces(hovertemplate="%{y}")
            fig_annual.update_layout(width=1100, height=500)
            fig_annual.layout.xaxis.fixedrange = True
            fig_annual.layout.yaxis.fixedrange = True
            fig_annual.update_traces(textposition="top center")
            fig_annual.update_traces(line_color="#147852")
            st.markdown(
                "<h2 style='text-align: center'>Number of deaths per year</h2>",
                unsafe_allow_html=True,
            )
            nb_current_year = tdor_data[tdor_data["year"] == current_year][
                "nb_victims_year"
            ].values[0]
            st.metric(
                label="Number of victims for current year",
                value=nb_current_year)
            st.plotly_chart(fig_annual, use_container_width=True)

        else:
            fig_annual = px.line(
                tdor_data,
                x="year",
                y="nb_victims_year",
                labels={
                    "nb_victims_year": "Number of victims yearly",
                    "year": "Years"},
            )
            fig_annual.layout.xaxis.fixedrange = True
            fig_annual.layout.yaxis.fixedrange = True
            fig_annual.update_traces(mode="markers+lines")
            fig_annual.update_layout(hovermode="x unified")
            fig_annual.update_layout(hoverlabel={"font_size": 14})
            fig_annual.update_traces(line_color="#040801")
            fig_annual.update_traces(hovertemplate="%{y}")
            fig_annual.update_layout(width=1100, height=500)
            fig_annual.update_traces(textposition="top center")
            fig_annual.update_traces(line_color="#147852")
            st.markdown(
                "<h2 style='text-align: center'>Number of deaths per year</h2>",
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_annual, use_container_width=True)
with st.container():
    col1, col2 = st.columns(2, gap="large")
    with col2:
        st.markdown(
            "<h2 style='text-align: center'>Number of deaths by categories per year</h2>",
            unsafe_allow_html=True,
        )

        if current_date < tdor_display:
            selected_cat = st.multiselect(
                "Show category",
                prev_years_data.Category.unique().tolist(),
                ["Violence", "Suicide"],
            )

            df_cat = prev_years_data[prev_years_data["Category"].isin(
                selected_cat)]
            fig_categorie_exepted_current = px.line(
                df_cat,
                x="year",
                y="nb_victims_Category_year",
                color="Category",
                text=df_cat["percentage_category"].apply(
                    lambda x: "{0:1.1f}%".format(x)
                ),
                labels={
                    "nb_victims_Category_year": " Number of deaths",
                    "year": "Years",
                },
            )
            fig_categorie_exepted_current.update_layout(width=1000, height=500)
            fig_categorie_exepted_current.layout.xaxis.fixedrange = True
            fig_categorie_exepted_current.layout.yaxis.fixedrange = True
            fig_categorie_exepted_current.update_traces(
                mode="markers+lines", hovertemplate=None
            )
            fig_categorie_exepted_current.update_layout(hovermode="x unified")
            fig_categorie_exepted_current.update_layout(
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="auto", x=0.5
                ),
            )
            st.plotly_chart(
                fig_categorie_exepted_current,
                use_container_width=True)
            categories = [
                "Violence",
                "Suicide",
                "Uncategorised",
                "Medical",
                "Custodial",
            ]
            for category in categories:
                count = (
                    tdor_data[tdor_data["year"] == current_year]["Category"]
                    .value_counts()
                    .get(category, 0)
                )
                if count > 0:
                    st.write(
                        f"Number of victims by {category} for {current_year}: {count}"
                    )
                else:
                    st.write(
                        f"No victims of {category} were reported for {current_year}."
                    )
        else:
            selected_cat_all = st.multiselect(
                "Show category",
                tdor_data.Category.unique().tolist(),
                ["Violence", "Suicide"],
            )
            df_cat = tdor_data[tdor_data["Category"].isin(selected_cat_all)]
            fig_categorie_y = px.line(
                df_cat,
                x="year",
                y="nb_victims_Category_year",
                color="Category",
                text=df_cat["percentage_category"].apply(
                    lambda x: "{0:1.1f}%".format(x)
                ),
                labels={
                    "nb_victims_Category_year": " Number of deaths",
                    "year": "Years",
                },
            )
            fig_categorie_y.update_layout(width=1000, height=500)
            fig_categorie_y.update_traces(
                mode="markers+lines", hovertemplate=None)
            fig_categorie_y.update_layout(hovermode="x unified")
            fig_categorie_y.layout.xaxis.fixedrange = True
            fig_categorie_y.layout.yaxis.fixedrange = True
            fig_categorie_y.update_layout(
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="auto", x=0.5
                )
            )
            st.plotly_chart(fig_categorie_y, use_container_width=True)
with col1:
    st.markdown(
        "<h2 style='text-align: center'>Distribution of deaths by categories</h2>",
        unsafe_allow_html=True,
    )
    data = (
        tdor_data.sort_values(["nb_victims_Category"], ascending=False)
        .groupby("Category")
        .head(3)
        .drop_duplicates("Category", keep="last")
    )
    distribution_cat = px.bar(
        data,
        x="nb_victims_Category",
        y="Category",
        color="Category",
        text=(data["percentage_category"].sort_values(ascending=False)).apply(
            lambda x: "{0:1.1f}%".format(x)
        ),
        labels={"nb_victims_Category": "Number of deaths per category"},
    )
    distribution_cat.update_layout(showlegend=False)
    distribution_cat.update_layout(hoverlabel={"font_size": 14})
    distribution_cat.update_layout(width=1000, height=500)
    distribution_cat.update_traces(hoverinfo="skip", hovertemplate=None)
    st.plotly_chart(distribution_cat, use_container_width=True,
                    config=dict({"staticPlot": True}))