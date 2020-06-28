import requests
import json

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

def hello2():
    return "Hello world2"

def postrequest():
    url1="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/delivery_quotes"
    url2="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/deliveries"

    #https://postmates.com/developer/docs/#resources__delivery__create-delivery

    params = 
    {
      'dropoff_address': '30 Providence Blvd, Kendall Park NJ, 08824'
      'pickup_address': '9 Bernadette Circle, Monmouth Junction, 08852'
    }

    r = requests.post(url1, params=params)

    if r.status_code != 200:
      print("Error:", r.status_code)

    data = r.json()
    return data