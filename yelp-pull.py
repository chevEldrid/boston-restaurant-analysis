#!/usr/bin/env python

import requests
import csv
import json

APIKEY = "vTUQpBRCeTkWwiTjb5zHIFuhkNJH-9NMHQcEzkErbo7ZJsOEJ-sSx1p20U_1hANtyoOuFwVV6B87XE0cZjCREb76UhfBMqv_ROqJhO6PrX61FNzUOUb3-A99kFOeXHYx"
CLIENTID = "aqikgLsOQ2RhlEkE6B0gRA"
#Boston zipcodes
ZIPLIST = ["02151","02152","02129","02128","02113","02114","02203","02110","02109","02108","02111","02116","02210","02199","02115","02215","02118","02127","02120","02119","02125","02122","02121","02130","02131","02126","02136","02467","02135","02134","02163"]
#
Offset = 0

f = csv.writer(open("test.csv", "wb+"))
#Write CSV Header
f.writerow(["Name", "Rating", "Price", "Category", "Lat", "Long", "City", "Address", "Zip"])
for zipc in ZIPLIST:
	while Offset < 1000:
		headers = {'Authorization': 'Bearer %s' % APIKEY}
		url_params = {'location':zipc, 'offset':Offset, 'limit': '50', 'term':'food'}
		r = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers,params=url_params)
		x = json.loads(r.text)
		places = x["businesses"]
		Offset += 50;
		#print(places)
		for i in places:
			#bc many categories...
			cat = i["categories"]
			gories = ""
			for l in cat:
				gories = (gories + l["title"] + ", ")
			gories = gories[:-2]
			#separate lat and longitude
			coords = i["coordinates"]
			#separate for address, city, and zip
			loc = i["location"]
			#deal with price if field doesn't exist or isn't populated
			price = ""
			try:
				price = i["price"].encode('utf8')
			except Exception as e:
				price = "-----"
			#deal with encoding parameters...see if that is causing issue
			name = ""
			try:
				name = i["name"].encode('utf8')
			except Exception as e:
				name = "-----"
			#deal with address
			address = ""
			try:
				address = loc["address1"].encode('utf8')
			except Exception as e:
				address = "-----"
			#print(cat)
			f.writerow([name, i["rating"], price, gories, coords["latitude"], coords["longitude"], loc["city"], address, loc["zip_code"]])
	Offset = 0
	print("Filled out all entries for: " + zipc)