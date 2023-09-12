import requests
import getpass
import json
import random

response = requests.get(
    'https://appeears.earthdatacloud.nasa.gov/api/product')
product_response = response.json()
# print(product_response)

json.dumps(product_response[0])
loc = input('location: ')
geoloc = requests.get('https://geocode.maps.co/search?q={' + loc + '}')
print(geoloc.json())

username = 'mcdepth'
pswd = 'VgZ#MNYz5&Fv$@TPF!q*kJCeKw' # getpass.getpass('Password: ')

response = requests.post('https://appeears.earthdatacloud.nasa.gov/api/login', auth=(username, pswd))
token_response = response.json()
print(token_response)

token = token_response['token']
response = requests.get(
    'https://appeears.earthdatacloud.nasa.gov/api/task', 
    headers={'Authorization': 'Bearer {0}'.format(token)})
task_response = response.json()
print(task_response)

product_id = 'SRTMGL1_NUMNC.003'
response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/product/{0}'.format(product_id))
layer_response = response.json()
print(layer_response)

ranProd = random.choice(product_response)
ranProd

response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/product/{0}'.format(ranProd['ProductAndVersion']))
layer_response = response.json()
print(layer_response)

response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/spatial/proj')
proj_response = response.json()
print(proj_response)

response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/quality/{0}'.format(ranProd['ProductAndVersion']))
quality_response = response.json()
print(quality_response)

quality_response[0]['QualityLayers'][0]

response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/quality/{0}/{1}'.format(quality_response[0]['ProductAndVersion'], quality_response[0]['QualityLayers'][0]))
quality_response = response.json()
print(quality_response)

quality_value = 0
response = requests.get('https://appeears.earthdatacloud.nasa.gov/api/quality/{0}/{1}/{2}'.format(quality_response[0]['ProductAndVersion'], quality_response[0]['QualityLayer'][0], quality_value))
quality_response = response.json()
print(quality_response)