#setup
# $virtualenv .
# $virtualenv venv --distribute
# $source venv/bin/activate
# $cd Desktop/geocode
# $pip install requests[security]
# $pip install geocoder
# $pip install ratelimit
# $python
# >>> import geocode_facilities
# >>> geocode_facilities.do

import geocoder
import csv
import time
from ratelimit import rate_limited


@rate_limited(0.5) #this package limits the rate of calls to google's API
def do():
	output=[]
	with open("facilities.csv", "rU") as file:
		reader = csv.reader(file)
		facilities_list = list(reader)
	for facility in facilities_list:
		#make address
		address=facility[0]+", "+facility[1]+", "+facility[2]+", "+facility[3]
		#make city
		city=facility[1]+", "+facility[2]+", "+facility[3]
		#default is to use penetentiary address, not city address
		city_indicator=0
		
		#Make call to googl api
		g = geocoder.google(address, timeout=10.0)

		#This if statement handles failures
		#failures caused by exceeding rate limit 
		if g.latlng==[]:
			g = geocoder.google(city, timeout=10.0)
			if g.latlng==[]:
				lat, lng = "none", "none"
				print "failed: ",
				print address,
				print g.latlng
			else:
				city_indicator=1
				lat=g.latlng[0]
				lng=g.latlng[1]
		else:
			lat=g.latlng[0]
			lng=g.latlng[1]
		output.append([address, lat, lng, city_indicator])

	with open("facility_locations.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(output)

