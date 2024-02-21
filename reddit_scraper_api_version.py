from apify_client import ApifyClient, ApifyClientAsync
import asyncio
import os
import requests
import time
import aiohttp

# Simple module, input the JSON input of the reddit scraper via the docs here : {https://apify.com/trudax/reddit-scraper/api/client/python} and then input that into the apify_reddit_agent method to get the returned value of the scrape.
APIFY_API_KEY = os.getenv("APIFY_API_KEY")
subreddit_search_json = {
    "debugMode": False,
    "includeNSFW": True,
    "maxComments": 5,
    "maxCommunitiesCount": 2,
    "maxItems": 50,
    "maxPostCount": 5,
    "maxUserCount": 5,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": [
            "RESIDENTIAL"
        ]
    },
    "scrollTimeout": 40,
    "searchComments": False,
    "searchCommunities": True,
    "searchPosts": False,
    "searchUsers": False,
    "searches": [
        "vietnam", "war", "Art"
    ],
    "skipComments": False
}


async def apify_reddit_agent_async(json_input, wait_time : int) :    
    async def call_scrape_request() : 
        url = f"https://api.apify.com/v2/acts/trudax~reddit-scraper-lite/runs?token={APIFY_API_KEY}"
        async with aiohttp.ClientSession() as session : 
            async with session.post(url, json=json_input) as response : 
                return await response.json()
    run_info = await call_scrape_request()
    async def get_json_information(defaultDatasetId) :
        max_atempts = 5 
        attempt = 0
        async with aiohttp.ClientSession() as session : 
            while max_atempts >= attempt : 
                attempt += 1
                url = f"https://api.apify.com/v2/datasets/{defaultDatasetId}/items?token=apify_api_fKZ25ERj0eKmcONf6XJtjoGbrLbL7s1WrYyh"
                print("waiting for data...")
                await asyncio.sleep(wait_time)
                async with session.get(url) as response: 
                    json_return = await response.json()
                    return json_return
    json_output = await get_json_information(run_info['data']['defaultDatasetId'])
    return json_output
    

# test = asyncio.run(apify_reddit_agent(subreddit_search_json, wait_time=60))
# print(test)
# test = apify_reddit_agent_async(subreddit_search_json)



# test_result = asyncio.run(test)
# print(test_result)

# test2 = apify_reddit_agent(subreddit_search_json)
# print(test2)