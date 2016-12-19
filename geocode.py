import googlemaps
from keys import *

# we get up to 5 thousand calls
locations = ['Right beside you. ', 'Moline, IL', 'Port Huron Michigan', 'Southern California', 'new joke city', 'Santa Rosa, Ca', 'Sunny CA', 'Marbella Andalucia Spain', 'Wyoming, MI', 'Little Rock, AR', 'los angeles', 'Saint Louis area', 'Misfit Toys Island', 'Brooklyn, NY', 'Hello, hello...here we go ', 'Jacksonville FL', 'Omaha, NE', 'new joke city', 'United States', 'Ventura CA', 'United States', 'Myrtle Beach', 'Saint Louis area', 'San Diego, CA', 'New York City,US/Heidelberg,DE', 'world Wide Web']

gmaps = googlemaps.Client(key=geocode_api_key)
coordinates = []
for location in locations:
	geocode_results = gmaps.geocode(location)
	#this returns 1 or 0 results, unclear as to why it comes back as an array
	for gresult in geocode_results:
		lat = gresult['geometry']['location']['lat']
		lng = gresult['geometry']['location']['lng']
		coordinates.append((lat, lng))
print(coordinates)