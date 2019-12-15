# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import folium
from folium import plugins
import requests

#GEO NUMBERS PER COUNTRY
geography = {'DK' : "50046",
             'NO' : "2978650",
             'SE': "52822",
             'IS' : "299133",
             'DE' : "51477",
             'NL' : "2323309",
             'SP' : "1311341",
             'EN' : "58447",
             'IT' : "365331",
             'PT' : "295480",
             'FO' : "52939",
             'FR' : "2202162"}

# READ CSV AND WRITE NEW
countries = {'DK' : 0, 'NO' : 0, 'SE' : 0, 'IS' : 0, 'DE' : 0, 'NL' : 0, 'SP' : 0, 'EN' : 0, 'IT' : 0, 'PT' : 0, 'FO' : 0, 'FR' : 0}
exceptions = [ ]
settlements = { }
data_file = r'origPlace_red.csv'
data = pd.read_csv(data_file)
for i in range(0, len(data)):
    country = data.iloc[i]['country1']
    try:
        countries[country] += 1
    except:
        if country is not np.nan:
            exceptions.append(country)
            print(country)
    if data.iloc[i]['settlement1'] is not np.nan:
        if data.iloc[i]['settlement1'] not in settlements.keys():
            settlements[data.iloc[i]['settlement1']] = {'total' : 0, 'lat' : data.iloc[i]['lat1'], 'lon' : data.iloc[i]['lon1']}
        settlements[data.iloc[i]['settlement1']]['total'] += 1
print(countries)
print(settlements)

f = open("number_of_docs.csv", "w+")
f.write("Country,Number\n")
for key in countries.keys():
    f.write(key + "," + str(countries[key]) + "\n")
f.close()

mss = r'number_of_docs.csv'
mss_data = pd.read_csv(mss)

geography_features = [ ]
for key in geography.keys():
    print(key)
    country_data = requests.get("http://polygons.openstreetmap.fr/get_geojson.py?id=" + str(geography[key]) + "&params=0").json()
    geography_features.append({'type':'Feature','geometry':country_data,'properties':{'name':key, 'number' : countries[key]}})

geography_data = ({'type':'FeatureCollection','features':geography_features})

m = folium.Map(location=[51,10], zoom_start=3)
folium.Choropleth(geo_data=geography_data, data=mss_data, columns=['Country','Number'], key_on='feature.properties.name', fill_color="YlGnBu", bins=[0,10,50,100,200,500,800], highlight=True).add_to(m)

layer = folium.FeatureGroup(name='layer')

#for index, row in mss_data.iterrows():
#    c = folium.GeoJson(
#        geography_data,
#        overlay=True,
#        style_function = lambda x : {'fillColor' : '#ffffff',
#                                 'color' : '#000000',
#                                 'fillOpacity' : 0.1,
#                                 'weight' : 0.01},
#        highlight_function = lambda x: {'fillColor' : '#000000',
#                                    'color' : '#000000',
#                                    'fillOpacity' : 0.5,
#                                    'weight' : 0.1},
#        )
#    folium.Popup('{}\n{}'.format(row['Country'], row['Number'])).add_to(c)
#    c.add_to(layer)
#layer.add_to(m)

#NIL = folium.GeoJson(
#    geography_data,
#    style_function = lambda x : {'fillColor' : '#ffffff',
#                                 'color' : '#000000',
#                                 'fillOpacity' : 0.1,
#                                 'weight' : 0.01},
#    highlight_function = lambda x: {'fillColor' : '#000000',
#                                    'color' : '#000000',
#                                    'fillOpacity' : 0.5,
#                                    'weight' : 0.1},
#    tooltip=folium.GeoJsonTooltip(
#        fields=['name', 'number'],
#        aliases=['Country: ', 'Number of Manuscripts: '],
#        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
#        sticky=True
#        )
#    )

#m.add_child(NIL)
#m.keep_in_front(NIL)
#folium.LayerControl().add_to(m)

cluster = folium.plugins.MarkerCluster(name="Settlements").add_to(m)

for key in settlements.keys():
    folium.Marker(location=[settlements[key]['lat'], settlements[key]['lon']], popup=key + ': ' + str(settlements[key]['total'])).add_to(cluster)

m.save('MSS_map.html')
    
