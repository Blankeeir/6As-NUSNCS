import datetime
import requests
import json
import os
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

AccountKey = os.getenv("ACCOUNT_KEY")
accept = 'application/json'
_headers = {'AccountKey': AccountKey, 'accept': accept}
start_date = '20220101'
end_date = '20230315'
date_format = '%Y%m%d'
start = datetime.datetime.strptime(start_date, date_format)
end = datetime.datetime.strptime(end_date, date_format)
delta = datetime.timedelta(days=1)
current_date = start
rainfallUrl = 'https://api.data.gov.sg/v1/environment/rainfall'
trafficFlowUrl = 'http://datamall2.mytransport.sg/ltaodataservice/TrafficFlow'
ERPRateUrl = 'http://datamall2.mytransport.sg/ltaodataservice/ERPRates'
def requestAndWriteToFile(url, file_name, relative_file_path):
    folder_path = os.path.join(os.path.dirname(__file__), relative_file_path)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    res = requests.get(url, headers=_headers)
    with open(file_path, 'w') as file:
        json.dump(res.json(), file)

def process_date(date):
    relative_file_path = '../../../data/static/rainfall/' + date.strftime('%Y/%m')
    requestAndWriteToFile(rainfallUrl, date.strftime('%d.json'), relative_file_path)
def getTrafficFlow():
    relative_file_path = '../../../data/static/traffic_flow'
    res = requests.get(trafficFlowUrl, headers=_headers)
    link = res.json()['value'][0]['Link']
    requestAndWriteToFile(link, 'traffic_flow.json', relative_file_path)
def getERPRate():
    relative_file_path = '../../../data/static/erp_rate'
    requestAndWriteToFile(ERPRateUrl, 'erp_rate.json', relative_file_path)
# Use concurrent.futures to run the process_date function in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Create a list of dates to process
    dates = []
    while current_date <= end:
        dates.append(current_date)
        current_date += delta

    # Submit the process_date function for each date to the executor
    results = [executor.submit(process_date, date) for date in dates]
    #results = []
    results.append(executor.submit(getTrafficFlow))
    results.append(executor.submit(getERPRate))

    # Wait for all tasks to complete
    concurrent.futures.wait([executor.submit(getERPRate)])
print("done")
