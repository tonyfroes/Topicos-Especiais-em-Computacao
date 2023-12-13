import requests
import csv
from geopy.distance import geodesic
import googlemaps
import time
from unidecode import unidecode
from selenium import webdriver
from functions import save_options, select_source, test_dados

def get_ip_from_csv():
  with open('Probes ISP Tools - Sheet.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    ip_list = []
    for row in csv_reader:
      ip_list.append(row[2])
    return ip_list
  
def get_prov_from_csv():
    prov_list = []
    with open('Probes ISP Tools - Sheet.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        prov_list = []
        for row in csv_reader:
            prov_list.append(row[1])
        return prov_list

def get_location_from_ip(ip):
    time.sleep(1)
    response = requests.get(f'http://ip-api.com/json/{ip}').json()
    location_data = {
        "city": response.get("city"),
        "region": response.get("region"),
    }
    return location_data

def get_distance_between_locations(location1, location2):
    # print('origem: ', location1)
    # print('destino: ', location2)
    distance = gmaps.distance_matrix(location1, location2)['rows'][0]['elements'][0]['distance']['value']/1000
    return distance

api_key = 'MY_API_KEY'
gmaps = googlemaps.Client(key=api_key)

ip_list = get_ip_from_csv()
prov_list = get_prov_from_csv()

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://isp.tools/traceroute")

# print(ip_list)

f = open('information.csv', 'w')
writer = csv.writer(f)

# print('len ip_list: ', len(ip_list))
# print('len prov_list: ', len(prov_list))

for ip in ip_list:

    distance = 0
    
    header = []

    for i in range(0, len(ip_list)-1):
        location1 = get_location_from_ip(ip)
        city1 = unidecode(location1["city"]) + " - " + location1["region"]
        
        location2 = get_location_from_ip(ip_list[i])
        city2 = unidecode(location2["city"]) + " - " + location2["region"]
        
        if ip != ip_list[i] and city1 != city2:
            print('ip: ', ip)
            print('ip_list: ', ip_list[i])

            distance = get_distance_between_locations(city1, city2)
            distance = round(distance, 2)

            media = test_dados(driver, ip, prov_list[i])

            sum = 0

            for i in range(len(media)):
                sum += media[i]
                if i == len(media)-1:
                    sum = round(sum/i)

            print(media, ' = ', sum)

            hop = len(media)

            ping = round(distance / 100)

            print(f'A distância entre {location1["city"]} e {location2["city"]} é {distance} quilômetros e o ping esperado é de {ping}ms\n')

            header.append([location1["region"], city1, ip, city2, ip_list[i], distance, ping, sum, hop])

        csv_file = 'information.csv'

        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Escreve os dados na lista no arquivo CSV
            writer.writerows(header)

    print('')
    writer.writerow('\n')
f.close()