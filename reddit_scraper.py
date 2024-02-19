from apify_client import ApifyClient, ApifyClientAsync
import asyncio
import os
# Simple module, input the JSON input of the reddit scraper via the docs here : {https://apify.com/trudax/reddit-scraper/api/client/python} and then input that into the apify_reddit_agent method to get the returned value of the scrape.
APIFY_API_KEY = os.getenv("APIFY_API_KEY")
print(APIFY_API_KEY)
subreddit_search_json = {
    "debugMode": False,
    "includeNSFW": True,
    "maxComments": 5,
    "maxCommunitiesCount": 1,
    "maxItems": 5,
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


def apify_reddit_agent(json_input) :    
    info_array = []
    #Changed the API key here to the samuel account instead.
    client = ApifyClient('apify_api_w727jhNXMt5mdg2rc5pfxkSBX2syyM01D6jc')

    run_input=json_input

    print("calling API endpoint")
    run = client.actor("trudax/reddit-scraper-lite").call(run_input=run_input)
    print("looping through items...")
    for item in client.dataset(run["defaultDatasetId"]).iterate_items() : 
        info_array.append(item)
    return info_array 

async def apify_reddit_agent_async(json_input) :    
    info_array = []
    #Changed the API key here to the samuel account instead.
    client = ApifyClientAsync('apify_api_w727jhNXMt5mdg2rc5pfxkSBX2syyM01D6jc')

    run_input=json_input

    print("calling API endpoint")
    run = await client.actor("trudax/reddit-scraper-lite").call(run_input=run_input)
    print("looping through items...")
    async for item in client.dataset(run["defaultDatasetId"]).iterate_items() : 
        info_array.append(item)
    return info_array 

    # test = apify_reddit_agent_async(subreddit_search_json)

    # test_result = asyncio.run(test)
    # print(test_result)
