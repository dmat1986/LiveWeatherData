import requests
import json
from math import cos, asin, sqrt
import datetime

#######################
#Test data
#######################

#latitude and longitude
lat=str(40.7700)
lng=str(-73.9000)

#time
time = datetime.datetime.now()

#######################
#Gets the conditions and temperature based on the latitude, 
#longitude, and time from the US National Weather Services API
#######################
def get_weather(lat,lng, time):
   #Obtain the correct gridpoint
   url = 'https://api.weather.gov/points/'+lat+','+lng
   r = requests.get(url)
   r=r.json()
   gridid=r["properties"]["gridId"]
   gridx=r["properties"]["gridX"]
   gridy=r["properties"]["gridY"]
   gridid=str(gridid)
   gridx=str(gridx)
   gridy=str(gridy)

   #Obtain the list of observation stations using the gridpoint
   obs_url = 'https://api.weather.gov/gridpoints/'+gridid+'/'+gridx+','+gridy+'/stations'
   g=requests.get(obs_url)
   gg=g.json()

   #Find the nearest observation station 
   dataArray=gg["features"]
   list_ = []
   v_lat = []
   v_lng = []

   count = len(dataArray)

   for j in range(count):
      for i in dataArray:
         v_lat.append(float(i["geometry"]["coordinates"][1]))
         v_lng.append(float(i["geometry"]["coordinates"][0]))
      list_.append({'lat':v_lat[j],'lng':v_lng[j]})

   #Find the nearest coordinates using the Haversine formula
   def distance(lat1, lon1, lat2, lon2):
      p = 0.017453292519943295
      hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
      return 12742 * asin(sqrt(hav))
   def closest(data, v):
      return min(data, key=lambda p: distance(v['lat'],v['lng'],p['lat'],p['lng']))

   our_data = {'lat':float(lat),'lng':float(lng)}
   comp_data = list_
   closest_coord = closest(comp_data,our_data)

   nearest_lat = closest_coord["lat"]
   nearest_lng = closest_coord["lng"]

   for i in dataArray:
      if float(i["geometry"]["coordinates"][1]) == nearest_lat and float(i["geometry"]["coordinates"][0]) == nearest_lng:
         station = i["id"]
   
   #Obtain the identifier of the nearest observation station
   station = requests.get(station)
   station = station.json()
   station_name = station["properties"]["stationIdentifier"]

   #Obtain the weather based on the time
   time=time.isoformat()
   time=time+'Z'

   cond_url='https://api.weather.gov/stations/'+station_name+'/observations?start='+time+'&limit=1'
   cond = requests.get(cond_url)
   cond = cond.json()
   condition = cond["features"][0]["properties"]["textDescription"]
   temp = cond["features"][0]["properties"]["temperature"]["value"]

   return [condition,temp]

#Call the function
condition=get_weather(lat,lng,time)[0]
temperature=get_weather(lat,lng,time)[1]

#Print the results
print(condition)
print(str(temperature)+" degrees celcius")
