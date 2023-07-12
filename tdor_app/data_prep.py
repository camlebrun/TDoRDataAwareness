import requests
import pandas as pd


class DataCollector:
    """Classe permettant de collecter les données"""

    def __init__(self, url):
        """Initialisation de la classe"""
        self.url = url

    def get_data(self):
        """téléchargement des données et préparation des données"""
        response = requests.get(self.url)
        data = response.json()
        pre_data = pd.DataFrame(data['data']['reports'])
        pre_data = pre_data[['name', 'age', 'birthdate', 'date',
                             'country', 'category', 'cause', 'permalink']]
        pre_data.rename(
            columns={
                'birthdate': 'Birthdate',
                'date': 'Date',
                'country': 'Country',
                'category': 'Category',
                'cause': 'Cause_of_death'},
            inplace=True)
        pre_data["Date"] = pd.to_datetime(pre_data["Date"])
        pre_data["year"] = pre_data["Date"].dt.year
        pre_data = pre_data[pre_data['year'] >= 1999]
        pre_data["nb_victims_year"] = pre_data.groupby(
            'year').year.transform("count")
        pre_data["nb_victims_Category"] = pre_data.groupby(
            'Category').Category.transform("count")
        pre_data["nb_victims_country"] = pre_data.groupby(
            'Country').Country.transform("count")
        pre_data["nb_victims_country_year"] = pre_data.groupby(
            ['Country', 'year']) .year.transform("count")
        pre_data["nb_victims_category_country"] = pre_data.groupby(
            ['Country', 'Category']) .Country.transform("count")
        pre_data["nb_victims_category_country_year"] = pre_data.groupby(
            ['Country', 'year', 'Category']).year.transform("count")
        pre_data["nb_victims_Category_year"] = pre_data.groupby(
            ['Category', 'year']).year.transform("count")
        pre_data["nb_victims_cause_year"] = pre_data.groupby(
            ['Cause_of_death', 'year']).year.transform("count")
        pre_data["Birthdate"] = pd.to_datetime(pre_data["Birthdate"]).dt.strftime('%Y-%m-%d')
        pre_data["year_birthdays"] = pd.to_datetime(pre_data["Birthdate"]).dt.year
        pre_data["total"] = len(pre_data)
        pre_data["age_cal"] = pre_data["year"] - pre_data["year_birthdays"]
        pre_data["Category"] = pre_data.Category.str.capitalize()
        pre_data["Cause_of_death"] = pre_data.Cause_of_death.str.capitalize()
        pre_data['percentage_category'] = (
            (pre_data["nb_victims_Category_year"] /
             pre_data["nb_victims_year"]) *
            100).round(1)
        df_pop = pd.read_csv('tdor_app/population_world.csv', low_memory=False)
        df_pop.reset_index(inplace=True)
        df_pop.drop(['SortOrder',
                     'LocID',
                     'Notes',
                     'ISO3_code',
                     'ISO2_code',
                     'SDMX_code',
                     'LocTypeID',
                     'LocTypeName',
                     'ParentID',
                     'VarID',
                     'MidPeriod',
                     'PopMale',
                     'PopFemale',
                     'PopDensity'], axis=1, inplace=True)
        df_pop = df_pop[df_pop['Variant'] == 'Medium']
        df_pop["PopTotal"] = (df_pop["PopTotal"] * 1000).astype(int)
        df_pop.drop(['Variant'], axis=1, inplace=True)
        df_pop.rename(columns={'Location': 'Country', 'Time': 'Year',
                               'PopTotal': 'Population'}, inplace=True)
        df_pop['Country'] = df_pop['Country'].replace(
            ['United States of America'], 'USA')
        tdor_merge_pop = df_pop.merge(
            pre_data, left_on=[
                'Year', 'Country'], right_on=[
                'year', 'Country'], how='right')
        tdor_merge_pop["Year"] = tdor_merge_pop["Year"].astype('Int64')
        tdor_merge_pop["ratio"] = (
            tdor_merge_pop["nb_victims_country_year"]
            / tdor_merge_pop["Population"]) * 100000
        tdor_merge_pop["ratio"] = tdor_merge_pop["ratio"].round(3)
        return tdor_merge_pop

    def suicide_data(self):
        """Pour les suicides"""
        suicide_data = self.get_data()
        # filter by category
        suicide_data = suicide_data[suicide_data['Category'] == 'Suicide']
        suicide_data["Date"] = pd.to_datetime(suicide_data["Date"])
        suicide_data["ratio"] = (
            suicide_data["nb_victims_category_country_year"]
            / suicide_data["Population"]) * 100000
        suicide_data["ratio"] = suicide_data["ratio"].round(5)
        return suicide_data

    def violence_data(self):
        """Pour les maps"""
        violence_data = self.get_data()
        violence_data = violence_data[violence_data['Category'] == 'Violence']
        violence_data["Date"] = pd.to_datetime(violence_data["Date"])
        violence_data["ratio"] = (
            violence_data["nb_victims_category_country_year"]
            / violence_data["Population"]) * 100000
        violence_data["ratio"] = violence_data["ratio"].round(5)
        return violence_data

    def custodial_data(self):
        'Head map'
        custodial_data = self.get_data()
        custodial_data = custodial_data[custodial_data['Category']
                                        == 'Custodial']
        custodial_data["ratio"] = (
            custodial_data["nb_victims_category_country_year"]
            / custodial_data["Population"]) * 100000
        custodial_data["ratio"] = custodial_data["ratio"].round(5)
        return custodial_data

    def medical_data(self):
        'Head map'
        medical_data = self.get_data()
        medical_data = medical_data[medical_data['Category'] == 'Medical']
        medical_data["ratio"] = (
            medical_data["nb_victims_category_country_year"] /
            medical_data["Population"]) * 100000
        medical_data["ratio"] = medical_data["ratio"].round(5)
        return medical_data

    def Uncategorised_data(self):
        'Head map'
        Uncategorised_data = self.get_data()
        Uncategorised_data = Uncategorised_data[Uncategorised_data['Category']
                                                == 'Uncategorised']
        Uncategorised_data["ratio"] = (
            Uncategorised_data["nb_victims_category_country_year"]
            / Uncategorised_data["Population"]) * 100000
        Uncategorised_data["ratio"] = Uncategorised_data["ratio"].round(5)
        return Uncategorised_data
