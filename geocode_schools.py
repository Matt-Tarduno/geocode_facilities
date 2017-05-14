#setup
# $virtualenv venv --distribute
# $source venv/bin/activate
# $cd Desktop/geocode
# $pip install requests[security]
# $pip install geocoder
# $python geocode_schools.py

import geocoder
import csv
import time
from ratelimit import rate_limited

@rate_limited(1) #this package limits the rate of calls to google's API
def do():
	output=[]
	with open("schools.csv", "rU") as school_file:
		reader = csv.reader(school_file)
		school_list = list(reader)
	for school in school_list:
		school_name=school[1]
		place_name=school[0]

		#clean up school names 
		if school_name.endswith("High"):
			school_name+=" School"
		if school_name.endswith("Middle"):
			school_name+=" School"
		if school_name.endswith("Elementary"):
			school_name+=" School"

		#make address	
		address=school_name+' '+place_name+", CA"
		print(address)

		#Make call to googl api
		g = geocoder.google(address, timeout=10.0)

		#This if statement handles failures
		#failures caused by exceeding rate limit 
		if g.latlng==[]:
			lat, lng = "none", "none"
			print "failed: ",
			print address,
			print g.latlng
			time.sleep(60)
			attempts=0
			while attempts<5:
				time.sleep(10)
				g = geocoder.google(address, timeout=20)
				if g.latlng!=[]:
					lat=g.latlng[0]
					lng=g.latlng[1]
					print(" fixed!")
					break
				attempts+=1
		else:
			lat=g.latlng[0]
			lng=g.latlng[1]
		output.append([address, lat, lng])

	with open("school_locations.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(output)

if __name__ == '__main__':
    do()


