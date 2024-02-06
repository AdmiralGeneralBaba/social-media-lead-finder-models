import requests 
import pandas as pd
twitter_data = [] 
payload = {
    'api_key' : 'd6b78dd3bb5f0a25162f42a646fd1782',
    'query' : 'test',
    'num' : '20'
}
response = requests.get(
    'https://api.scraperapi.com/structured/twitter/search', params=payload
)
data = response.json()
print(data)
print( len(data['organic_results']))