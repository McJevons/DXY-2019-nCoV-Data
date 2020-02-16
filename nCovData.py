#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[9]:


class nCovData():
    def __init__(self, filename):
        self.data = pd.read_csv(filename)

    def get_df_by_cities(self, *cities):
        df = self.data[[
            'cityName', 'city_confirmedCount', 'city_suspectedCount',
            'city_curedCount', 'city_deadCount', 'updateTime'
        ]]
        df = df.drop(df[~df['cityName'].isin(cities)].index)
        df['updateTime'] = df['updateTime'].map(lambda x: x[:10])

        df_cities = pd.DataFrame([])
        for city in cities:
            df_city = df.drop(df[df['cityName'] != city].index)

            df_city = df_city.groupby(['updateTime']).max()

            df_city['city_increase_confirmed'] = df_city[
                'city_confirmedCount'].diff(1).fillna(0)

            df_cities = df_cities.append(df_city)

        df_cities = df_cities.pivot(columns='cityName').fillna(0)

        return df_cities

    def get_full_df(self):
        return self.data