import requests
import json
import sys
from classes import ErrorResponseGenerator, SuccessResponseGenerator


def get_view(viewId, apiKey):
    url = f"https://api.gridly.com/v1/views/{viewId}"
    payload = {}
    headers = {
    'Authorization': f'ApiKey {apiKey}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.ok:
        return json.loads(response.text)
    else:
        return response
    
def create_column(viewId, apiKey, lang_code, languageType):
    url = f"https://api.gridly.com/v1/views/{viewId}/columns"

    payload = json.dumps({
    "id": lang_code,
    "name": lang_code,
    "type": "language",
    "languageCode": lang_code,
    "localizationType": languageType
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'ApiKey {apiKey}'
    }

    #response = requests.request("POST", url, headers=headers, data=payload)
    return send_call("POST", url, headers, payload)

def upload_records_into_gridly(viewId, apiKey, records):
    url = f"https://api.gridly.com/v1/views/{viewId}/records"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'ApiKey {apiKey}'
    }
    _records = []
    for record in records:
        _records.append(record)
        if len(_records) == 999:
            send_call("POST", url, headers, json.dumps(_records))
            _records.clear()
    if len(_records) > 0:
        send_call("POST", url, headers, json.dumps(_records))

    
    #success_generator = SuccessResponseGenerator(len(records))
    #print(success_generator.get_response_json())



def get_dependencies(viewId, apiKey):
    url = f"https://api.gridly.com/v1/views/{viewId}/dependencies"

    payload = {}
    headers = {
    'Authorization': f'ApiKey {apiKey}'
    }

    #response = requests.request("GET", url, headers=headers, data=payload)
    return send_call("GET", url, headers, payload)

def create_dependency(viewId, apiKey, sourceColumnId, targetColumnId):
    url = f"https://api.gridly.com/v1/views/{viewId}/dependencies"

    payload = json.dumps({
        "sourceColumnId": sourceColumnId, 
        "targetColumnId": targetColumnId
        })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'ApiKey {apiKey}'
    }
    return send_call("POST", url, headers, payload)
    #response = requests.request("GET", url, headers=headers, data=payload)

def export_view_as_csv(viewId, apiKey):
    url = f"https://api.gridly.com/v1/views/{viewId}/export"

    payload = {}
    headers = {
    'Authorization': f'ApiKey {apiKey}'
    }
    return send_call("GET", url, headers, payload)

def send_call(method, url, headers, payload):
    #print(method, url, headers, payload)
    response = requests.request(method, url, headers=headers, data=payload)
    if response.ok:
        if "export" in url:
            return response.text
        else:
            return json.loads(response.text)
        
    else:
        error_generator = ErrorResponseGenerator(response.status_code, "API", json.loads(response.text)["message"])
        print(error_generator.get_response_json())
        sys.exit()