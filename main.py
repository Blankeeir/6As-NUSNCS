import asyncio
import os
import time
import json
import threading

from dotenv import load_dotenv
import requests
from controller.controller import Controller
from web_api.dialogue_api import dialogue_api_handler
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS


threads = []
load_dotenv()
AccountKey = os.getenv("ACCOUNT_KEY")
accept = 'application/json'
_headers = {'AccountKey': AccountKey, 'accept': accept}
pwd = os.path.dirname(os.path.abspath(__file__))
print(pwd)

def requestAndWriteToFile(url, file_name, relative_file_path, withLink=False):
    folder_path = os.path.join(pwd, relative_file_path)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    res = requests.get(url, headers=_headers)
    if withLink:
        link = res.json()['value'][0]['Link']
        res = requests.get(link, headers=_headers)
    with open(file_path, 'w') as file:
        json.dump(res.json(), file)

def update(api):
    interval = api['interval']
    url = api['url']
    file_name = api['name'] + '.json'
    relative_file_path = "data/dynamic/" + api['name']
    withLink = False
    if 'withLink' in api:
        withLink = api['withLink']
    params = [""]
    if 'params' in api:
        params = api['params']
def temp():
    while True:
        print("Updating " + file_name)
        requestAndWriteToFile(url, file_name, relative_file_path, withLink)
        time.sleep(interval)

t = threading.Thread(target=temp)
threads.append(t)
t.start()

app = Flask(__name__)
api = Api(app)
CORS(app)

dialogue_api_hl = dialogue_api_handler()

parser = reqparse.RequestParser()
parser.add_argument('user_input',type=str,location='json')

def respond(res):
    return {'code':0,'message':'success','res':res}

def chat(query):
    try:
        res = dialogue_api_hl.generate_massage(query)
        return respond(res)
    except Exception as e:
        return {'code':1,'message':'fail','res':'!!! The api call is abnormal, please check the backend log'}

#print(chat("hello"))

@app.route("/ping")
def ping():
    return "Pong"

@app.route("/echo")
def echo():
    args = parser.parse_args()
    user_request_input = args['user_input']
    return respond(user_request_input)


MainController = Controller()

async def run():
    file_paths = [
        "data/static/rainfall/2023/03/15.json",
        "data/static/Traffic Flow.json",
        "data/static/erp_rate/erp_rate.json"
    ]

    tasks = [
        asyncio.create_task(app.run(host='0.0.0.0', port=80, debug=True)),
        asyncio.create_task(MainController.get_real_time_data()),
        asyncio.create_task(periodic_task(file_paths[0])),
    ]
    await asyncio.gather(*tasks)
async def periodic_task(file_path):
    while True:
        await MainController.get_static_data(file_path)
        await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(run())


