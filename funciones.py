
Librerías

import pandas as pd
import numpy as np
import re
import os
import pymysql
from sqlalchemy import create_engine
import getpass
import matplotlib.pyplot as plt
import pprint
from bs4 import BeautifulSoup


import requests #para hacer las llamadas apis
import os #para moverte por el ordenador
from dotenv import load_dotenv #para cargar fichero env
load_dotenv() 
git_token = os.getenv("git_token")

origin = pd.read_csv(('../your-code/Input/report.csv'), engine = 'python')
origin.head()  

columns = origin.columns
print(columns)
print(origin.shape)

new = origin["agency_jurisdiction"].str.split(", ", n = 1, expand = True)

result = pd.concat([origin, new], axis=1, sort=False)

crimen = result.rename(columns={0: "state", 1: "sig"})
display(crimen.head())

res = requests.get("https://www.worldatlas.com/articles/the-most-dangerous-states-in-the-u-s.html")

data = res.text

soup = BeautifulSoup(data, 'html.parser')

tabla = soup.select('#tableToggle')

see = soup.select('#artReg-table > table:nth-child(1)')
html = soup.find_all("tbody")

crimen_paises = []
for fila in soup.find_all('tbody'):
    filas = [el for el in fila.find_all('tr')]
    if len(filas) > 0:
        for fila in filas:
            datos = fila.find_all('td')
            crimen = {
                "Rank":int(datos[0].text),
                "State": datos[1].text.strip(),
                "violence_rate":int(datos[2].text)

            }
            crimen_paises.append(crimen)       
crimen_paises   
crimen_scrap = pd.DataFrame(crimen_paises)

crimenscrapt = crimen_scrap.rename(columns={"State": "states"})
crimenscrapt.head()


scrapstates = {"states" : ["Alaska", "New Mexico", "Nevada", " Tennessee", "Louisiana", "Arkanas", "Alabama",
                           "Missouri", "Delaware", "South Carolina", "Maryland", "Arizona", "Michigan", 
                           "Oklahoma", "California", "Illinois", "Texas", "Florida", "South Dakota", "Indiana", 
                           "Georgia", "Kansas", "Massachusetts", "New York", "North Carolina", "Montana", 
                           "West Virginia","Colorado", "Pennsylvania", "Hawaii", "Wisconsin", "Washington",
                           "Ohio", "Nebraska", "Iowa", "Mississippi", "Oregon", "North Dakota", "New Jersey",
                           "Wyoming", "Utah",  "Minnesota", "Rhode Island", "Kentucky", "Idaho", "Connecticut",
                           "Virginia", "New Hampshire", "Vermont", "Maine"], "sig" : ["AL", "NM", "NV", "TN", "LA", "AR", "AL", "MO", "DE", "SC", "MD", "AZ", "MI", "OK", "CA",
                     "IL", "TX", "FL", "SD", "IN", "GA", "KS", "MA", "NY", "NC", "MT", "WV", "CO", "PA", "HI",
                     "WI", "WA", "OH", "NE", "IA", "MS", "OR", "ND", "NJ", "WY", "UT", "MN",  "RI", "KY", "ID",
                     "CT", "VA", "NH", "VT", "ME"]}                       
                           
states_acron = pd.DataFrame(scrapstates)
states_acron. head()

mergescrap = pd.merge(states_acron, crimenscrapt , how='left', on=['states'])
mergescrap.head()

mergestot = pd.merge(crimen, mergescrap , how = "left", on = ["sig"])
mergestot.head()



mergestot["months_reported"].value_counts()

cleanorigin = mergestot.drop(columns=["violent_crimes", "homicides", "rapes", "assaults","robberies"] )
cleanorigin
# Eliminar las siguientes columnas pues las que me interesan son aquellas que se mide por el ratio per-capital
#violent_crimes, homicides, rapes, assaults, robberies.
region = cleanorigin.groupby('sig', as_index=True).agg({'crimes_percapita':'mean','violence_rate':'mean' ,'homicides_percapita':'mean','rapes_percapita':'mean','assaults_percapita':'mean', 'robberies_percapita':'mean'})
region
violent = region.sort_values('crimes_percapita', ascending=False)
violence = violent.iloc[0:5]
violence

violence.index
violence.plot.bar()

crimenes = region.sort_values('violence_rate', ascending=False)
crimenesscr = crimenes.iloc[0:5]
crimenesscr

crimenesscr.index
crimenesscr.plot.bar()

homic = violent[["homicides_percapita"]]
homicides = homic.sort_values('homicides_percapita', ascending=False)
homicid = homicides.iloc[0:5]
homicid


homicid.index
homicid.plot.bar()

rap = violent[["rapes_percapita"]]
rapes = rap.sort_values('rapes_percapita')
rape = rapes.iloc[0:5]
rape



rape.index
rape.plot.bar()


assa = violent[["assaults_percapita"]]
assaults = assa.sort_values('assaults_percapita', ascending=False)
assau = assaults.iloc[0:5]
assau

assau.index
assau.plot.bar()

rob = violent[["robberies_percapita"]]
robberies = rob.sort_values('robberies_percapita', ascending=False)
robs = robberies.iloc[0:5]
robs


robs.index
robs.plot.bar()


