from v1_subreddits_finder import stage_3_final
from reddit_scraper_api_version import apify_reddit_agent_async
from openai_calls import OpenAI
import asyncio
import copy
import re

#global variables
test_url_array = ['https://www.reddit.com/r/Entrepreneur/', 'https://www.reddit.com/r/startups/', 'https://www.reddit.com/r/datascience/', 'https://www.reddit.com/r/Marketing_Strategies/', 'https://www.reddit.com/r/LeadGeneration/']

subreddit_search_json = {
    "debugMode": False,
    "includeNSFW": True,
    "maxComments": 0,
    "maxCommunitiesCount": 1,
    "maxItems": 150,
    "maxPostCount": 300, 
    "maxUserCount": 300,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": [
            "RESIDENTIAL"
        ]
    },
    "scrollTimeout": 40,
    "searchComments": False,
    "searchCommunities": False,
    "searchPosts": True,
    "searchUsers": False,
    "skipComments": False,
    "startUrls": [
       
    ]
}

urls = ['https://www.reddit.com/r/Erookie/', 'https://www.reddit.com/r/PMBuddy/', 'https://www.reddit.com/r/digital_marketing/']

async def stage_4_scrape_posts(subreddit_urls) : 
    tasks = []
    for url in subreddit_urls: 
        new_json = copy.deepcopy(subreddit_search_json)
        new_json['startUrls'].append({'url' : url})
        print(new_json)
        tasks.append(apify_reddit_agent_async(json_input=new_json, wait_time=180))
    print(new_json)
    scraped_posts_array = await asyncio.gather(*tasks)
    flattened_array = [item for array in scraped_posts_array for item in array]
    return flattened_array


# return_values = asyncio.run(stage_4_scrape_posts( urls)) 
# print(return_values)



    



# test_body = """ Does anyone else feel like tech has gotten toxically competitive?
# I just feel like it’s impossible to convince people to try new things anymore. I think people have become so burnt out by crypto/ai/whatever grifts that everything that isn’t already owned by FAANG is worthless.

# I’ll tell my friends about a new technology or an innovation I’m working on and they treat me like I’m trying to throw acid in their face. Or like it’s their god given duty to find the one flaw an idea has and make sure I know it’ll be worthless because of it.

# It’s starting to impact my feeling towards being an entrepreneur. I don’t even know if I want to create new innovations if each new customer has to be dragged kicking and screaming from the status quo."""

# test_problem = """We """



# test = stage_5_evaluate_post(test_problem, test_body)

# print(test)





# scrapped_posts = stage_4_scrape_posts(test_url_array)
# print(scrapped_posts)   