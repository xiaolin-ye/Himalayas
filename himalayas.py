# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:04:05 2022

@author: xy
"""

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
 
#%%
# loc = Nominatim(user_agent="GetLoc")
# def get_coord(name):
    
#     getLoc = loc.geocode(name)
    
#     if getLoc is not None:
#         # printing address
#         print(getLoc.address)
         
#         # printing latitude and longitude
#         print("Latitude = ", getLoc.latitude, "\n")
#         print("Longitude = ", getLoc.longitude) 
#         return getLoc.latitude, getLoc.longitude
#     else:
#         return 'na', 'na'
 
peaks = pd.read_csv('peaks.csv',dtype={'first_asc_yr': str})

n_peaks = len(peaks)

print(peaks['height_m'].mean())
pct_climbed = len(peaks[peaks['climb_status'] == 'Climbed'])/n_peaks     
pct_unclimbed = len(peaks[peaks['climb_status'] == 'Unclimbed'])/n_peaks  


sorted_peaks = peaks.sort_values('height_m', ascending=False)
# highest_peaks = sorted_peaks.head(20)
# highest_peaks = highest_peaks[["peak_id","peak_name",
#                                    "host_contries","height_m",
#                                    "location","climb_status",
#                                    "first_asc_yr"]]

sorted_peaks = sorted_peaks[["peak_id","peak_name",
                                    "host_contries","height_m",
                                    "location","climb_status",
                                    "first_asc_yr"]]


# lat_vect = []
# lon_vect = []

# for i in range(0,len(highest_peaks)):
#     lat, lon = get_coord(highest_peaks.iloc[i].get('location'))
#     lat_vect.append(lat)
#     lon_vect.append(lon)


year_count = peaks.groupby('first_asc_yr')['peak_id'].count().sort_values()
year_count = year_count.drop(['0','201'])

year_count.to_csv('yearly_climbed_peaks.csv')

sorted_peaks.to_csv('sorted_by_height.csv', header=['ID', 'Name','Contries','Height', 'Location', 'Status', 'Ascending Year'])


#%%
expeditions = pd.read_csv('expeditions.csv')

expeditions = expeditions[['peak_id','peak_name','nationality','year','season',
                                 'host_cntr','sponsor','leaders','is_commercial_rte',
                                 'exp_result','summit_days','total_mbrs','mbrs_summited',
                                 'mbrs_deaths','is_o2_not_used']]


expeditions.columns = ['ID', 'Peak', 'Country', 'Year', 'Season', 'Host', 'Sponsor',
                       'Leaders', 'Commercial', 'Result', 'Days', 'Members', 'Members Summited',
                       'Members Deaths', 'O2 Usage']

expedition_evolution = expeditions.sort_values(['Year', 'Peak','Country', 'Season'],
                                               ascending=False).groupby([
                                                   'Year', 'Peak','Country', 'Season'])['Peak'].count()

expedition_evolution.to_csv('expedition_country_counts.csv')


expedition_yearly_country = expeditions.sort_values(['Country', 'Year'], ascending=False).groupby(['Country','Year'])['Peak'].count()
expedition_yearly_country.to_csv('expedition_yearly_country.csv')
expedition_yearly = expeditions.sort_values(['Year'], ascending=False).groupby(['Year'])['Peak'].count()
expedition_yearly.to_csv('expedition_yearly.csv')

iscommercial = expeditions.sort_values(['Commercial'],ascending=False).groupby(['Commercial'])['Peak'].count()
iscommercial = pd.DataFrame(iscommercial).transpose()
iscommercial.columns = ['No', 'Yes']
iscommercial = iscommercial.transpose()
iscommercial['Metric'] = 'Commercial'

host = expeditions.sort_values(['Host'],ascending=False).groupby(['Host'])['Peak'].count()
host = pd.DataFrame(host)
host['Metric'] = 'Host'

result = expeditions.sort_values(['Result'],ascending=False).groupby(['Result'])['Peak'].count()
result = pd.DataFrame(result)
result['Metric'] = 'Result'

o2usage = expeditions.sort_values(['O2 Usage'],ascending=False).groupby(['O2 Usage'])['Peak'].count()
o2usage = pd.DataFrame(o2usage).transpose()
o2usage.columns = ['Yes', 'No']
o2usage = o2usage.transpose()
o2usage['Metric'] = 'O2 Usage'

expedition_conditions = pd.concat([iscommercial, host, result, o2usage])
expedition_conditions.to_csv('expedition_conditions.csv')


#%%

deaths = pd.read_csv('deaths.csv')

deaths = deaths[['peak_name','yr_season','gender','age','cause_of_death']]
deaths['yr_season'] = deaths.yr_season.str.replace(r' .*', r'')
deaths['cause_of_death'] = deaths.cause_of_death.str.replace(r'\(\d.*', r'')

deaths.columns = ['Peak', 'Year', 'Gender', 'Age', 'Cause']
deaths_summary = deaths.sort_values(['Cause', 'Gender'],ascending=False).groupby(['Cause', 'Gender'])['Peak'].count()
deaths_summary.to_csv('death_summary.csv')
