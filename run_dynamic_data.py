import os
import time
import json
import time
import json
import threading

from dotenv import load_dotenv
import requests

threads = [] 
load_dotenv()
AccountKey = os.getenv("ACCOUNT_KEY")
accept = 'application/json'
_headers = {'AccountKey': AccountKey, 'accept': accept} 
def requestAndWriteToFile(url, file_name, relative_file_path, withLink=False):
    folder_path = os.path.join(os.path.dirname(__file__), relative_file_path)
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
    while True:
        for param in params:
            _url = url + param
            def temp():
                while True:
                    requestAndWriteToFile(_url, file_name, relative_file_path, withLink)
                    time.sleep(interval)
            t = threading.Thread(target=temp)
            threads.append(t)
            t.start()

apis = None
with open("data/dynamic/apis.json", 'r') as file:
    apis = json.load(file)

for api in apis:
    update(api)