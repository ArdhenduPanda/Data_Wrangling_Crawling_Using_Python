from googleplaces import GooglePlaces, types, lang
import googlemaps
from datetime import datetime
import re
import requests
from googletrans import Translator

#file="C:/Users/girijamohanty/Documents/Signalling/Data/re_bank_bangalore.txt"
file1="C:/Users/girijamohanty/Documents/Signalling/Data/re_ATM_bangalore_final_dummy.csv"
fileWrite=open(file1,'w')
YOUR_API_KEY = 'AIzaSyDROd9drCGfq0XP2RN0xsW5tOHVJ5yS4K8'
google_places = GooglePlaces(YOUR_API_KEY)
gmaps = googlemaps.Client(key=YOUR_API_KEY)
GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
places_list=["ACCELERATE MOTORS,Rajarajeshwari Nagar",
"ACCELERATE MOTORS, Kengeri",
"ACCLAIM MOTORS PVT LTD,Bellary Rd",
"BOMMASANDRA MOTORS,Bommasandara Industrial Area",
"CVS MOTORS,HRBR Layout",
"CVS MOTORS,Bellary Road",
"CVS MOTORS HEBBAL,Bhadrappa Layout",
"ELECTRONIC CITY MOTORS,Hosur Main Road",
"HSR SERVICES,Lalbagh Road",
"HSR SERVICES,BSK 2nd Stage",
"HSR SERVICES,Rajajinagar",
"KORMANGALA MOTORS,Hosur Main Rd",
"ROYAL ENFIELD BRAND STORE,Jayanagar",
"ROYAL ENFIELD BRAND STORE,BTM 2nd Stage",
"ROYAL ENFIELD COMPANY STORE,Malleswaram",
"SAI RAM AUTOCRAFT,DV Nagar",
"SR MOTORS,Nagarbhavi",
"SRI SADHGURU SAI MOTORS,Nelamangla",
"SRI SADHGURU SAI MOTORS,Dasarahalli",
"TEKNIK MOTORCYCLES,Sarjapur Road",
"TEKNIK MOTORS,Hoskote",
"TEKNIK MOTORS,Indiranagar",
"WHITEFIELD MOTORS,KR Puram Hobli"]

pincode_list=[
'560098',
'560060',
'560064',
'560099',
'560043',
'560080',
'560094',
'560068',
'560027',
'560070',
'560010',
'560029',
'560069',
'560076',
'560003',
'560016',
'560072',
'562123',
'560057',
'560102',
'562114',
'560038',
'560066'
]
pincode_list_bangalore=[560059, 560001, 560002, 560003, 560004, 560005, 560006, 560007, 560008, 560009, 560010, 560011, 560012, 560013, 560014, 560015,
 560016, 560017, 560018, 560019, 560020, 560021, 560022, 560023, 560024, 560025, 560026, 560027, 560028, 560029, 560030, 560032, 560033, 560034, 560036,
 560037, 560038, 560039, 560040, 560041, 560042, 560043, 560045, 560046, 560047, 560048, 560049, 560050, 560051, 560052, 560053, 560054, 560055, 560056,
 562106, 562107, 560058, 560061, 560062, 560063, 560064, 560065, 560066, 560067, 560068, 560069, 560070, 560071, 560072, 560073, 560074, 560075, 560076,
 562125, 560078, 560079, 560077, 560080, 562130, 560083, 560084, 560085, 560086, 560087, 560091, 560092, 560093, 560094, 560095, 560096, 560097, 560098,
 560099, 560100, 562149, 560102, 560103, 560104, 562157]
#pincode_list_bangalore=[560017]
f=0
fileWrite.write("College Name"+","+"Pincode"+","+"College Location"+","+"GeoTag"+","+"AddressLine"+","+"City"+","+"District"+","+"State"+","+"Country"+","+"PostalCode"+"\n")
#fileWrite.write("Outlet Name"+","+"Pincode"+","+"Location"+","+"GeoTag"+"\n")
translator = Translator()

while f < len(pincode_list_bangalore):
    query_result = google_places.nearby_search(location=pincode_list_bangalore[f],keyword='ATM',radius=2000)#,types=[types.TYPE_PARK])
    if len(query_result.places)>0:
        for place in query_result.places:
            print(place.geo_location)
            #.encode("utf-8")
            params = {'latlng': str(re.findall(r'[-+]?\d*\.\d+|\d+', str(place.geo_location))[0])+','+str(re.findall(r'[-+]?\d*\.\d+|\d+', str(place.geo_location))[1]),'sensor': 'true','key':YOUR_API_KEY}
            req = requests.get(GOOGLE_MAPS_API_URL, params=params)
            print(req.json()['results'])
            res = req.json()['results'][0]
            #address=translator.translate(str(res['address_components']),dest='en').text
            address=res['address_components']
            postalCode=address[len(address)-1]['long_name']
            country=address[len(address)-2]['long_name']
            state=address[len(address)-3]['long_name']
            district=address[len(address)-4]['long_name']
            city=address[len(address)-5]['long_name']
            #addressLine=translator.translate(str(res['formatted_address']),dest='en').text
            addressLine=res['formatted_address']
            print("\""+str(place.name.encode("utf-8"))+"\",\""+str(pincode_list_bangalore[f])+"\",\""+str(tuple(re.findall(r'[-+]?\d*\.\d+|\d+', str(place.geo_location)))).strip()+"\",\""+str(place.place_id)+"\",\""+addressLine+"\",\""+city+"\",\""+district+"\",\""+state+"\",\""+country+"\",\""+postalCode+"\n")
            #print("\""+str(place.name.encode("utf-8"))+"\",\""+str(pincode_list_bangalore[f])+"\",\""+str(tuple(re.findall(r'[-+]?\d*\.\d+|\d+', str(place.geo_location)))).strip()+"\",\""+str(place.place_id)+"\"\n")
            fileWrite.write("\""+str(place.name.encode("utf-8"))+"\",\""+str(pincode_list_bangalore[f])+"\",\""+str(tuple(re.findall(r'[-+]?\d*\.\d+|\d+', str(place.geo_location)))).strip()+"\",\""+str(place.place_id)+"\",\""+
			.translate(str(addressLine),dest='en').text+"\",\""+city+"\",\""+district+"\",\""+state+"\",\""+country+"\",\""+postalCode+"\"\n")
            #fileWrite.write("\""+str(place.name.encode("utf-8"))+"\",\""+str(pincode_list_bangalore[f])+"\",\""+str(tuple(re.findall(r'[-+]?\d*\.\d+|\d+', str(place.geo_location)))).strip()+"\",\""+str(place.place_id)+"\"\n")
    f=f+1
fileWrite.close()

	
