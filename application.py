import requests
import json

from flask import Flask
app = Flask(__name__)

@app.route("/")

def index():
    url1="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/delivery_quotes"
    url2="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/deliveries"

    #https://postmates.com/developer/docs/#resources__delivery__create-delivery
  
  #This is the API KEY: ea6f0581-b447-459e-98cc-5c7b22a27335
    
    pickup_address = "9 Bernadette Circle, Monmouth Junction, 08852"
    dropoff_address = "30 Providence Blvd, Kendall Park NJ, 08824"
    quote_params = {
      "dropoff_address": dropoff_address,
      "pickup_address": pickup_address
    }

    quote_req = requests.post(url1, params=quote_params, auth=('ea6f0581-b447-459e-98cc-5c7b22a27335', ''))

    if quote_req.status_code != 200:
      print("Error:", quote_req.status_code)

    quote_id = quote_req.json()["id"]

    pickup_name = "Ashna's house"
    pickup_phone_number = "7324229194"
    dropoff_name = "Neha"
    dropoff_phone_number = "6098656754"
    manifest = "test items"
    '''
    manifest_items = [{
      "quantity": 1,
      "size": "medium",
      "name": "test"
    }]
    '''
    manifest_items = []
    #manifest_items.append(manifest_item)

    delivery_req = requests.post(url2, params=delivery_params, auth=('ea6f0581-b447-459e-98cc-5c7b22a27335', ''))
    return delivery_req.json()


'''
def hello():
    return "Hello World!"

def hello2():
    return "Hello world2"
'''