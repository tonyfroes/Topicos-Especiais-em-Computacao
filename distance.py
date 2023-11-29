import requests
import csv
from geopy.distance import geodesic
from geopy.distance import geodesic

def get_ip():
  response = requests.get('https://api64.ipify.org?format=json').json()
  return response["ip"]

def get_location():
  ip = get_ip()
  response = requests.get(f'https://ipinfo.io/{ip}/json').json()
  location_data = {
    "ip": ip,
    "city": response.get("city"),
    "region": response.get("region"),
    "country": response.get("country"),
    "latitude": response.get("loc").split(",")[0],
    "longitude": response.get("loc").split(",")[1]
  }
  return location_data

#create a funcion that saves in a list the ip from the 'Probes ISP Tools - Sheet1.csv' file
def get_ip_from_csv():
  with open('Probes ISP Tools - Sheet1.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    ip_list = []
    for row in csv_reader:
      ip_list.append(row[2])
    return ip_list

# create a function that gets the location of the ip from the list

def get_location_from_ip(ip):
  response = requests.get(f'https://ipinfo.io/{ip}/json').json()
  location_data = {
    "ip": ip,
    "city": response.get("city"),
    "region": response.get("region"),
    "country": response.get("country"),
    "latitude": response.get("loc").split(",")[0],
    "longitude": response.get("loc").split(",")[1]
  }
  return location_data

# create a function that gets the distance between two locations

def get_distance_between_locations(location1, location2):
  coords_1 = (location1["latitude"], location1["longitude"])
  coords_2 = (location2["latitude"], location2["longitude"])
  distance = geodesic(coords_1, coords_2).kilometers
  return distance

my_location = get_location()
ip_list = get_ip_from_csv()

for ip in ip_list:
  if ip == '-':
    ip_list.remove(ip)
  else:
    location = get_location_from_ip(ip)
    distance = get_distance_between_locations(location, my_location)
    distance = round(distance, 2)
    ping = round(distance/100)
    print(f'\nThe distance between {location["city"]} and {my_location["city"]} is {distance} kilometers and the ping is {ping} ms')