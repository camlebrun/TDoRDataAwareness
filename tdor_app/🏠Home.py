import streamlit as st
import requests

st.set_page_config(layout = "wide", page_title = "Home")
st.markdown("<h1 style='text-align: center'>When Data meet: transphobia around the world </h1>", unsafe_allow_html=True)

st.warning(icon='⚠️', body="It is important to note that the reported number of deaths among transgender individuals may not accurately reflect the true extent of the problem.")

st.markdown("<h2 style='text-align: center'>About TDoR</h2>", unsafe_allow_html=True)

st.markdown("Transphobia is the fear, hatred, or discrimination against transgender individuals or those perceived to be transgender. It can manifest in a variety of ways, from verbal abuse and harassment to physical violence and murder.")
st.markdown("The Transgender Day of Remembrance (TDoR) is an annual event that honors the memory of those who have been killed as a result of transphobia. The day is observed on November 20th and serves as a reminder of the ongoing violence and discrimination faced by transgender individuals around the world.")
st.markdown("The TDoR memorials and vigils serve several purposes. They help raise public awareness of hate crimes against transgender people, publicly mourn and honor the lives of our brothers and sisters who might otherwise be forgotten, and provide a space for transgender people and their allies to affirm their commitment to ending hate crimes.")
st.markdown("It is important to note that the TDoR is not just about remembering those who have died, but also about raising awareness and taking action to end transphobia and violence against transgender people. It's a time to reflect on the past and present, and to commit to creating a better future for transgender people everywhere.")
st.markdown("It's important for everyone to educate themselves about the issues faced by transgender individuals and to actively work to create a more inclusive and accepting society. This includes supporting transgender rights, speaking out against transphobia, and being an ally to the transgender community.")
st.markdown("<h2 style='text-align: center'>About my web app</h2>", unsafe_allow_html=True)

st.markdown("I have created a python web app using Streamlit and Plotly to display historical data of the Transgender Day of Remembrance (TDoR). The app allows users to view the data by year, category, and country.")

st.markdown("The app starts by displaying a summary of the total number of victims over the years and a graph showing the number of victims per year. Users can then filter the data by category, such as violence, suicide, medical and custodial, to view the number of victims in each category over the years. They can also filter the data by country to view the number of victims in each country over the years.")

st.markdown("The app also allows the user to select a specific year and see the number of victims by category and by country. The data is represented using interactive graphs that allow the user to hover over the data points to view the specific numbers.")

st.markdown("The app provides a powerful tool for understanding the impact of transphobia over the years and in different countries. It serves as a reminder of the ongoing violence and discrimination faced by transgender individuals around the world, and allows users to reflect on the past and present, and to commit to creating a better future for transgender people everywhere.")

st.markdown("I have used Streamlit to create the UI of the web app, which makes it easy to navigate and interact with the data. The data is represented using Plotly, which provides interactive and visually appealing graphs. The app is designed to be user-friendly and intuitive, making it easy to understand and interact with the data.")

st.markdown("Overall, this web app is a great resource for anyone who wants to understand the impact of transphobia on transgender individuals and to take action to end transphobia and violence against transgender people.")



st.markdown("<h4>Credit</h4>", unsafe_allow_html=True)

st.write("This text was written by ChatGPT and Camille Lebrun")
st.markdown("The data was collected by Translives Matter and can be found  [here](https://tdor.translivesmatter.info/reports).")
st.markdown("You can find the code for this app [here](https://github.com/camlebrun/tdor_project).")
st.markdown("You can find my web site and projects [here](https://camlebrun.github.io/).")
st.markdown("<h6>Camille Lebrun - 2023</h6>", unsafe_allow_html=True)
