from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

import requests
import json

url="http://example.com/index.php"

r = requests.post(url, params={'q': 'raspberry pi request'})



if r.status_code != 200:

  print "Error:", r.status_code



data = r.json()

example = data["value1"]["value2"]

print(example)