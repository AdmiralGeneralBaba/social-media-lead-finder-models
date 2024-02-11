from v1_subreddits_finder import stage_3_final
from reddit_scraper import apify_reddit_agent
from openai_calls import OpenAI
import re

#global variables
test_url_array = ['https://www.reddit.com/r/Erookie/    ', 'https://www.reddit.com/r/PMBuddy/', 'https://www.reddit.com/r/digital_marketing/', 'https://www.reddit.com/r/Sensory/', 'https://www.reddit.com/r/Marketresearch/']

subreddit_search_json = {
    "debugMode": False,
    "includeNSFW": True,
    "maxComments": 5,
    "maxCommunitiesCount": 1,
    "maxItems": 300,
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
    "searchCommunities": False,
    "searchPosts": True,
    "searchUsers": False,
    "skipComments": False,
    "startUrls": [
       
    ]
}

urls = ['https://www.reddit.com/r/Erookie/', 'https://www.reddit.com/r/PMBuddy/', 'https://www.reddit.com/r/digital_marketing/', 'https://www.reddit.com/r/Sensory/', 'https://www.reddit.com/r/Marketresearch/']

def stage_4_scrape_posts(subreddit_urls) : 
    new_json = subreddit_search_json.copy()
    for url in subreddit_urls: 
        new_json['startUrls'].append({'url' : url})
    print(new_json)
    scraped_posts = apify_reddit_agent(new_json)
    return scraped_posts

def stage_5_evaluate_post(problem, post_body) : 
    llm = OpenAI()
    temp = 0.96
    prompt = """take a deep breath. You will be given a problem that a model customer faces, and a post from reddit that talks about something. 
Your mission is to decide whether or not the post relates to the problem that the model customer faces. IF it does relate, then you are to respond with a 'YES' ONLY. 
IF it does relate, output ONLY 'NO'


e.g if the user's problem matches with the model customer problem, this should be your output : 

YES

otherwise, it should be : 
NO

Here is the model customer's problem :+ """ + "'" +  f"{problem}" + "'" +  """you should err on side of it matching the user problem.

And here is the post information : """
    response = llm.open_ai_gpt_call(post_body, prompt, temp)   
    print(response)
    yes_pattern = r"(YES)"
    matches = re.findall(yes_pattern, response) 
    if matches : 
        return True 
    return False
   
def v1_subreddit_scanner(subreddit_urls, problem) : 
    diluted_posts = []
    scraped_posts = stage_4_scrape_posts(subreddit_urls)
    for post in scraped_posts : 
        input_post_body = post['body']
        result = stage_5_evaluate_post(problem, input_post_body)
        if result == True : 
            diluted_posts.append(post)
    return diluted_posts




# def stage_6_evaluate_all_posts(problem, scraped_posts) : 
#     for post in scraped_posts : 
#         stage_5_evaluate_post()


    



test_body = """ Does anyone else feel like tech has gotten toxically competitive?
I just feel like it’s impossible to convince people to try new things anymore. I think people have become so burnt out by crypto/ai/whatever grifts that everything that isn’t already owned by FAANG is worthless.

I’ll tell my friends about a new technology or an innovation I’m working on and they treat me like I’m trying to throw acid in their face. Or like it’s their god given duty to find the one flaw an idea has and make sure I know it’ll be worthless because of it.

It’s starting to impact my feeling towards being an entrepreneur. I don’t even know if I want to create new innovations if each new customer has to be dragged kicking and screaming from the status quo."""

test_problem = """We """



test = stage_5_evaluate_post(test_problem, test_body)

print(test)





# scrapped_posts = stage_4_scrape_posts(urls)
# print(scrapped_posts)   