from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

'''
import requests
import json

url1="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/delivery_quotes"
url2="https://api.postmates.com/v1/customers/cus_MjTrLMXWncD3Rk/deliveries"

#https://postmates.com/developer/docs/#resources__delivery__create-delivery

r = requests.post(url, params={'q': 'raspberry pi request'})



if r.status_code != 200:

  print "Error:", r.status_code



data = r.json()

example = data["value1"]["value2"]

print(example)

'''