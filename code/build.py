########################################################
# IMPORT DATA AND MAKE PLOTS
########################################################

# IMPORTS
import numpy as np 
import pandas as pd 
import itertools as it 
import matplotlib.pyplot as plt 

# LOAD DATA
path = 'C:/Users/anikb/Dropbox/Active Projects/diseases/COVID-19/'
data_path = path+'csse_covid_19_data/'

data_GEO = pd.read_csv(data_path+'UID_ISO_FIPS_LookUp_Table.csv')
data_TS_confirmed = pd.read_csv(data_path+'csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
data_TS_deaths = pd.read_csv(data_path+'csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
url_confirmed = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths    = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_html(url_confirmed)[0]
deaths = pd.read_html(url_deaths)[0]
recovered = pd.read_html(url_recovered)[0]

# RESHAPE DATASETS
# Define places
confirmed_by_country = confirmed.groupby('Country/Region',as_index=False)[confirmed.columns[3:]].sum()
deaths_by_country = deaths.groupby('Country/Region',as_index=False)[deaths.columns[3:]].sum()
recovered_by_country = recovered.groupby('Country/Region',as_index=False)[recovered.columns[3:]].sum()

# Reshape routine
def reshape_data_long(dataset,reshape_i,dates,newvar):
    datasetL = pd.DataFrame(columns=reshape_i + [newvar])
    for date in dates:
        temp = dataset[reshape_i+[date]]
        temp = temp.rename(columns={date:newvar})
        temp['date'] = date
        datasetL = datasetL.append(temp)
    return datasetL

# Implement Reshape
dates = confirmed.columns[5:]
confirmed_long = reshape_data_long(confirmed_by_country,['Country/Region','Lat','Long'],dates,'confirmed')
deaths_long = reshape_data_long(deaths_by_country,['Country/Region','Lat','Long'],dates,'deaths')
recovered_long = reshape_data_long(recovered_by_country,['Country/Region','Lat','Long'],dates,'recovered')

# Create COVID Plots - By Country
def plot_TS(dataset,countries,var):
    for country in countries:
        temp = dataset.loc[dataset['Country/Region']==country,['Country/Region','date',var]]
        plt.plot(temp['date'],temp[var],label=country)

def plot_normalized_Ncases(dataset,countries,var,Ncases):
    for country in countries:
        temp = dataset.loc[dataset['Country/Region']==country,['Country/Region','date',var]]
        temp = temp.loc[temp[var]>=Ncases]
        temp = temp.reset_index()
        temp['date_relative'] = temp.index + 1
        plt.plot(temp['date_relative'],temp[var],label=country)

