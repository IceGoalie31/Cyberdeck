import requests
#import urllib.parse

#placeholder module
def datetime() -> object: #testing function
    city = 'chicago'
    api_url = 'https://api.api-ninjas.com/v1/worldtime?city={}'.format(city)
    response = requests.get(api_url, headers={'X-Api-Key': "YzRSvd4OLwJHSr387YyyyHM298XwXFhXrxYcKU7N"})
    res = response.json()
    if response.status_code == requests.codes.ok:
        return res['datetime']
    else:
        print("Error:", response.status_code, response.text)

def deauth():
    return "deauth"

def scanAP():
    return "scanap"
def scan():
    return "scan"

def deauth():
    return "deauth"