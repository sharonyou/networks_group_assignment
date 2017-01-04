import googlemaps
from keys import *
from models import Retweet, Reply, TrumpStatus, Hashtag


# JS to place in the function "getPoints"
# https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap#try-it-yourself
# function getPoints() {
# 	// these are coordinates from location_list_to_coordinate_list
# 	points = [[37.09024, -95.712891], [32.715738, -117.1610838], [32.3546679, -89.3985283], [33.4483771, -112.0740373], [46.1908484, -84.8314496], [34.3916641, -118.542586], [37.6456329, -84.77217019999999], [-23.3044524, -51.1695824], [28.5383355, -81.3792365], [44.3148443, -85.60236429999999], [39.7596061, -121.6219177], [36.0971945, -115.1466648], [36.778261, -119.4179324], [39.9611755, -82.99879419999999]];
#   	listMapPoints = [];
#   	for (var i = 0; i < points.length; i++) {
#   		lat = points[i][0];
#     		lng = points[i][1];
#   		mapPoint = new google.maps.LatLng(lat,lng)
#   		listMapPoints.push(mapPoint);
#  	 }
#   return listMapPoints;
# }

def location_list_to_coordinate_list(locations):
	# we only get up to 5,000 calls each day...
	gmaps = googlemaps.Client(key=geocode_api_key)
	coordinates = []
	for location in locations:
		geocode_results = gmaps.geocode(location)
		#this returns 1 or 0 results, unclear as to why it comes back as an array
		for gresult in geocode_results:
			lat = gresult['geometry']['location']['lat']
			lng = gresult['geometry']['location']['lng']
			coordinates.append([lat, lng])
	return coordinates



def get_reply_locations(trump_status_id):
	locations = []
	for reply in Reply.select().where(Reply.in_reply_to_status_id_str == trump_status_id).order_by(Reply.created_at):
		location = reply.location
		if location:
			locations.append(location)
	return locations

if __name__ == "__main__":
	nuclear_tweet_id = '811977223326625792'
	locations = get_reply_locations(nuclear_tweet_id)
	coordinates = location_list_to_coordinate_list(locations)
	print(coordinates)