import requests
import getpass
import json
import random

response = requests.get(
    'https://appeears.earthdatacloud.nasa.gov/api/product')
product_response = response.json()
print(product_response)