from openai_calls import OpenAI
import asyncio
import json
from reddit_scraper import apify_reddit_agent_async
import re

#global values : 
subreddit_search_json = {
    "debugMode": False,
    "includeNSFW": True,
    "maxComments": 0,
    "maxCommunitiesCount": 2,
    "maxItems": 2,
    "maxPostCount": 0,
    "maxUserCount": 0,
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



# Takes in the product description the user gave, and then returns a JSON/dictionary output with a users array of string values
def stage_1_end_user_description(product_description) : 
    llm = OpenAI()
    prompt = """ From the product description inputted, give 3 users who will find this product useful.
When you give your output, it must be in this dictionary format :

{ "users" : [

{"user" : "{output here}"},
{"user" : "{output here}"}
etc
]
}

ONLY output this and nothing else."""
    temp = 1
    users = llm.open_ai_gpt4_turbo_call(product_description, prompt, temp)
    return users



def stage_2_keyword_generation(users) : 
    llm = OpenAI()
    prompt = """ based on these target customer types, Give 3 keywords for each customer type to search on reddit for relevant communities. For each user input in the JSON given, you are to add a new field called 'keywords' structured like this : 
    "keywords" : [{keyword 1}, {keyword 2}, etc]: 
    here is the JSON you will add to. Note. : """ 
    temp = 1 
    users_json_with_keywords = llm.open_ai_gpt4_turbo_call(users, prompt, temp)
    return users_json_with_keywords

def create_json_full(product_description) : 
    print("Getting end user description...")
    end_users = stage_1_end_user_description(product_description)
    print("Getting the keywords to search for subreddits...")
    keywords_addon = stage_2_keyword_generation(end_users)
    print("Here are the keywords : ", keywords_addon)
    print("Creating the JSON from the string...")

    def json_regex_remove(json) : 
      pattern = r'```|json|\s*json\s*'
      # Replace matched patterns with an empty string
      cleaned_text = re.sub(pattern, '', json)
      return cleaned_text
    processed_json = json_regex_remove(keywords_addon)
    input_json = json.loads(processed_json)
    return input_json

#Stage 3, reddit api calls

async def search_for_subreddits(keywords) : 
    tasks = []
    
    print("these are the keywords : ", keywords)
    for keyword in keywords :
      new_json = subreddit_search_json.copy()
      print("this is the keyword : ", keyword)
      single_keyword_array = [keyword]
      new_json["searches"] = single_keyword_array
      print(new_json)
      # Loads up the caroutines for the apify reddit scraping
      info = apify_reddit_agent_async(new_json)
      tasks.append(info)
    # Flatten the array (as the apify agent returns a array, adn then this is made into a array of arrays)#
    print(tasks)
    info_array = await asyncio.gather(*tasks)
    new_list = [item for subarray in info_array for item in subarray]
    return new_list

#Evaluator method for the pick local best stage : 
async def stage_3_evaluator_method(user, user_keyword_json) : 
  async def evaluate_local_subreddits(user_subreddits_json) :
      user_description = user['user']
      llm = OpenAI()
      prompt = """Based on the subreddits given, pick all the relevent ones that relate to this end-user description. Take into account ESPECIALLY the decription of the community; IT MUST relate to the end user.: """ + f"""{user_description}""" + """you MUST output in this format and nothing else :
{
"urls" : [
'url1',
'url2',
'url3'.
etc
]
}
2
"""
      temp = 1 
      input_json = json.dumps(user_subreddits_json)
      chosen_urls = await llm.async_open_ai_gpt4_turbo_call(input_json, prompt, temp)
      return chosen_urls
      
  def breakdown_json(json) :
    new_json = []
    for json in user_keyword_json : 
        if json['dataType'] != 'fake' :
          local_new_json = {
            "title" : json["title"],
            'description' : json['description'],
            'numberOfMembers' : json["numberOfMembers"],
            'url' : json['url']
          }
          new_json.append(local_new_json)
    return new_json

  new_json = breakdown_json(user_keyword_json)

  urls = await evaluate_local_subreddits(new_json)

  url_json = json.loads(urls)
  print(url_json)
  return url_json


    
# calls three scrapes for each of the users within the JSON, and inputs the keywords as the search inputs.

async def stage_3_reddit_api_calls(json) : 
    # Its calling three for each fo the usesrs in the json, need fto have it so that it calls them asll at once :  
    tasks = []
    async def search_and_evaluate(user) : 
      local_result = await search_for_subreddits(user['keywords'])
      print("this is the scrape from the stage 3 method : ", local_result)
      user_subreddits_json = await stage_3_evaluator_method(user, local_result)
      user.update(user_subreddits_json)
      print(local_result)
      return user
    for user in json['users'] :
        tasks.append(search_and_evaluate(user))
    return_json = await asyncio.gather(*tasks)
    return return_json

def stage_3_spread_url(json) : 
    urls = []
    for user in json : 
      urls.extend(user['urls'])
    print(urls)
    return urls


#Inputted is the product description, the search JSON is generated, then the API endpoints are called and the resutls are returned, then the JSON is formated in the correct way : 
async def stage_3_final(product_description) : 
  json = create_json_full(product_description=product_description)
  new_json = await stage_3_reddit_api_calls(json)
  print("this is the JSON value at stage_3_final : ", new_json)
  urls = stage_3_spread_url(new_json)
  return urls












# test_json = """```json
# {
#   "users": [
#     {
#       "user": "VFX studios looking to outsource rotoscoping work",
#       "keywords": ["rotoscoping", "VFX outsourcing", "postproduction services"]    
#     },
#     {
#       "user": "Independent filmmakers requiring professional VFX services",        
#       "keywords": ["indie filmmaking", "VFX services", "film postproduction"]      
#     },
#     {
#       "user": "Animation companies needing to supplement their in-house VFX teams",
#       "keywords": ["animation VFX", "VFX team augmentation", "visual effects assistance"]
#     }
#   ]
# }
# ```"""
# print(test_regex_remove(test_json))


########################## TESTING CODE ########################
# test_keywords = ['vietnam', 'china', 'japan']

# test_search = asyncio.run(search_for_subreddits(keywords=test_keywords))
# print(test_search)
# test_product_description = """ 'My startup aims to allow users to type in the problem that their product is supposed to solve, and then from this it searches multiple social media platforms and then returns to the user the leads that have posted/commented about their problem'"""
# json_test = create_json_full(product_description)
# print(json_test)

# stage_3_final(test_product_description)



# user_json = {
#   "users": [
#     { 
#       "user": "Startup founders looking to identify their target audience",
#       "keywords": ["startup advice", "customer discovery", "target market"]
#     },
#     {
#       "user": "Marketing professionals seeking to perform market analysis",
#       "keywords": ["market research", "marketing strategy", "consumer insights"]
#     },
#     {
#       "user": "Social media managers aiming to engage with potential customers",
#       "keywords": ["social media marketing", "audience engagement", "brand community"]
#     }
#   ]
# }

# user_json2 = {
#      "users": [
#     { 
#       "user": "Startup founders looking to identify their target audience",
#       "keywords": ["startup advice", "customer discovery", "target market"]
#     },
#     {
#       "user": "Marketing professionals seeking to perform market analysis",
#       "keywords": ["market research", "marketing strategy", "consumer insights"]
#     }
#   ]
# }

# test_json_2 = [{
#     "id": "2z6wn",
#     "name": "t5_2z6wn",
#     "title": "Streetwear Startup",
#     "headerImage": "https://a.thumbs.redditmedia.com/gq9561mrzeY9TrVx.png",
#     "description": "The underground community no one wants to admit they're from.\n\nThis subreddit serves to be a platform for streetwear brand owners (startups and established) to discuss ideas, trade knowledge, share your brand, and connect with others.",
#     "over18": False,
#     "createdAt": "2013-11-22T21:49:18.000Z",
#     "scrapedAt": "2024-02-07T18:20:58.179Z",
#     "numberOfMembers": 775612,
#     "url": "https://www.reddit.com/r/streetwearstartup/",
#     "dataType": "community"
# }]

# test_json_3 = [{
#   "id": "2xquw",
#   "name": "t5_2xquw",
#   "title": "Startup Business Advice",
#   "description": "Startup business advice and ideas ",
#   "over18": False,
#   "createdAt": "2013-07-02T13:51:45.000Z",
#   "scrapedAt": "2024-02-07T17:45:32.873Z",
#   "numberOfMembers": 77,
#   "url": "https://www.reddit.com/r/Erookie/",
#   "dataType": "community"
# },
# {
#   "id": "2ykna",
#   "name": "t5_2ykna",
#   "title": "Grow My Business",
#   "headerImage": "https://f.thumbs.redditmedia.com/ln2GJkQ_topvbCGY.png",
#   "description": "Welcome to r/growmybusiness. This is the place to find and share creative advice to optimize your business growth.",
#   "over18": False,
#   "createdAt": "2013-09-21T21:43:58.000Z",
#   "scrapedAt": "2024-02-07T17:45:32.984Z",
#   "numberOfMembers": 46562,
#   "url": "https://www.reddit.com/r/growmybusiness/",
#   "dataType": "community"
# }]

 
# test = stage_3_evaluator_method(user_json2['users'][0],test_json_3)
# print(test)

# links = stage_3_final(user_json2)
# print(links)


