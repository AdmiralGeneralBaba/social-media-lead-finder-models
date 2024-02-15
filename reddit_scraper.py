from apify_client import ApifyClient
# Simple module, input the JSON input of the reddit scraper via the docs here : {https://apify.com/trudax/reddit-scraper/api/client/python} and then input that into the apify_reddit_agent method to get the returned value of the scrape.

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
    client = ApifyClient('apify_api_caOfCyl6W2Sa205GuGGOpAZ3R1oseh1RLv9L')

    run_input=json_input

    print("calling API endpoint")
    run = client.actor("trudax/reddit-scraper-lite").call(run_input=run_input)
    print("looping through items...")
    for item in client.dataset(run["defaultDatasetId"]).iterate_items() : 
        info_array.append(item)
    return info_array 


# test = apify_reddit_agent(subreddit_search_json)
# print(test)