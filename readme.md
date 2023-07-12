# TDoR - Transgender Day of Remembrance

*This project was presented as part of my studies at HETIC.*
- [TDoR - Transgender Day of Remembrance](#tdor---transgender-day-of-remembrance)
  - [Context](#context)
  - [Objectives](#objectives)
  - [Deliverables](#deliverables)
    - [Presentation of each page:](#presentation-of-each-page)
  - [Issues and solutions](#issues-and-solutions)


## Context

"Dur à Queer" is a media outlet dedicated to defending the rights of Queer individuals. The outlet regularly covers issues related to gender and sexual identities, as well as affective and sexual lives. The 24th edition of TDoR (Transgender Day of Remembrance), a day of remembrance for transgender individuals, will take place on November 20, 2023. This day commemorates transgender individuals who have been murdered or committed suicide due to their gender identity. Unfortunately, these acts of violence often involve murders or suicides motivated by transphobia, and it is important to raise awareness of these tragedies. Statistics show that transphobia is an increasingly significant problem in many countries, and it is essential to raise public awareness of this reality. The media outlet believes that data visualization is a powerful tool for promoting empathy and action, and is eager to collaborate with the development team to create a superior-quality application.

## Objectives

* Create a data visualization application to present real-time data on TDoR (Transgender Day of Remembrance) victims
* Allow users to interactively explore the data and discover trends and information about the victims in real-time, via the TransLivesMatter association's API
* The addition of data, its updates as well as visualizations should be automatic (ie: no technical intervention required each year to update the written dates)
* Ensure the quality and credibility of information provided to the public by using reliable sources and adhering to the standards and norms of the transgender rights protection field.

## Deliverables

* Python code following the PEP 8 standard, available on GitHub
* A requirements.txt file including the technical configuration

### Presentation of each page:

**Page 1:** Introduction to the topic

**Page 2:** Presentation of real-time data: total number of people killed, average age, number of victims for the current year. Graphs will be added, and on each November 20th, the data for the current year will be added. Before November 20th, data from the previous years will be displayed. The following graphs will be displayed:

* A graph with historical data
* The distribution of deaths according to the categories in the database
* A representation of the distribution of deaths by year (with percentages)

**Page 3:** The data will be normalized (deaths/10,000 inhabitants). The population data for each country has been determined using data from the OECD (average data). The user will be able to choose the year, and three maps will be displayed:

* Total number of deaths
* Suicide
* Homicide

**Page 4:** Will allow the user to see the number of deaths by the selected country, with the percentage breakdown. Two bar charts will be available:

* Number of deaths per year
* Number of deaths per year by category

These graphs will be interactive and allow users to select specific years to view data in more detail. The percentage breakdown will also be displayed for each category. This will allow users to understand the proportion of each type of death in the selected country.

**Page 5:** The user can select the type of death. A normalized heatmap (death/100K inhabitants) will be displayed.

**Page 6:** Will allow the user to see the number of deaths at the current moment and by category. The user can choose a country to view in more detail.

**Page 7:** A search tool allowing the user to search for victim(s) by:

* Year
* Country
* Categories
* Name

**Page 8:** A search tool that allows users to search for victim(s) by their identity to access a profile created by TransLivesMatter.

**Page 9:** Allows users to compare the number of deaths in year Y-1 and Y-2.

**Page 10:** Users can select the year to access the number of deaths per month. An additional graph is added to show the median number of deaths per month since 1999 with the median across the 12 months.P

## Issues and solutions

Unfortunately, I have encountered several challenges in creating this project. The first major issue is the lack of complete data available for the victims of the TDoR. This is due to several factors such as data collection from relatives, the criminalization of trans identity in some countries, as well as the isolation of affected communities. Additionally, hyperlinks to commemorative pages were not available on page 7. They were not clickable as the hyperlink had to be associated with the name. Therefore, an additional page had to be created to address this issue.

To ensure reliable data visualization on page 2, only current year's data is visible on the day of TDoR. Another challenge is to ensure compatibility of the application with mobile devices, which is due to the complexity of the technology used. Moreover, the age of all victims is not available, which could affect the accuracy of data analysis. Therefore, it was not possible to analyze this parameter.

Finally, the application must have reasonable loading times to prevent users from losing interest or becoming frustrated with the service. To improve this, it is necessary to create DAGs with an AirFlow-like solution to store and refresh data every month.