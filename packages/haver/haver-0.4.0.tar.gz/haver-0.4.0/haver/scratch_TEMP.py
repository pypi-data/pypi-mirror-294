import os
os.environ['HAVER_API_KEY'] = 'wCT48fKMOeIbVZImPzzz32Ocrk4oEFMey9Um7xPVZw0'
import requests

HEADERS = {'Content-Type': 'application/json', 
           'X-API-Key':os.getenv('HAVER_API_KEY')}
_HAVER_URL = 'https://api.haverview.com'
database = 'EUDATA'


requests.get(
            f"{_HAVER_URL}/v4/database/{database}/series?&format=short&per_page=1000",
            headers=HEADERS).json()

database='EUDATA'
series='N997CE'
API_URL = f'{_HAVER_URL}/v4/database/{database}/series/{series}'

requests.get(API_URL, headers=HEADERS).json()



requests.get(f"{_HAVER_URL}/v4/database", headers=HEADERS).json()
x = requests.get(f"{_HAVER_URL}/v4/database/G10/series?&per_page=10000",headers=HEADERS).json()

x = requests.get(f"{_HAVER_URL}/v4/database/G10/series/B122VRM",headers=HEADERS).json()

[e for e in x['data']  if 'recess' in e['description'].lower()]

requests.get(f"{_HAVER_URL}/v4/database/G10/series/", headers=HEADERS).text#.json()







# NOT WORKING

requests.get(f"{_HAVER_URL}/v4/recessions", headers=HEADERS).text#.json()
requests.get(f"{_HAVER_URL}/v4/docs",
                      headers=HEADERS).json()['data']


query='defined'
requests.get(f"{_HAVER_URL}/v4/search?query={query}",headers=HEADERS).text#.json()
