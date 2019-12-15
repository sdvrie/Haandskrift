# -*- coding: utf-8 -*-
import pandas as pd
import folium
import requests

#GEO NUMBERS PER COUNTRY
geography = {'DK' : "50046",
             'NO' : "2978650",
             'SE': "52822",
             'IS' : "299133",
             'DE' : "51477",
             'NL' : "2323309",
             'SP' : "1311341",
             'EN' : "58447"}

# READ CSV AND WRITE NEW
countries = {'DK' : 0, 'NO' : 0, 'SE' : 0, 'IS' : 0, 'DE' : 0, 'NL' : 0, 'SP' : 0, 'EN' : 0}
exceptions = [ ]
data_file = r'origPlace_red.csv'
data = pd.read_csv(data_file)
for i in range(0, len(data)):
    country = data.iloc[i]['country1']
    try:
        countries[country] += 1
    except:
        if country not in exceptions:
            exceptions.append(country)
            print(country)
print(countries)

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
    geography_features.append({'type':'Feature','geometry':country_data,'properties':{'name':key}})

geography_data = ({'type':'FeatureCollection','features':geography_features})

m = folium.Map(location=[51,10], zoom_start=3)
folium.Choropleth(geo_data=geography_data, data=mss_data, columns=['Country','Number'], key_on='feature.properties.name', fill_color="YlGn").add_to(m)

m.save('../MSS_map.html')
    
