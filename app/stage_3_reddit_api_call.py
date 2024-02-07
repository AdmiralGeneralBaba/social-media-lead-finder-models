from reddit_scraper import apify_reddit_agent

subreddit_search_json = {
    "debugMode": False,
    "includeNSFW": True,
    "maxComments": 5,
    "maxCommunitiesCount": 5,
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
        
    ],
    "skipComments": False
}

def search_for_subreddits(keyword) : 
    new_json = subreddit_search_json.copy()
    new_json["searches"] = [keyword]
    
    info = apify_reddit_agent(new_json)
    return info

test_keyword = "housing"

test_search = search_for_subreddits(test_keyword)

print(test_search)