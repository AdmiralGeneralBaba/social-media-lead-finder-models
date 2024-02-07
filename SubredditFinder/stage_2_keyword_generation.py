from openai_calls import OpenAI
from stage_1_end_user_description import stage_1_end_user_description
import asyncio
import json

product_description = """ 'My startup aims to allow users to type in the problem that their product is supposed to solve, and then from this it searches multiple social media platforms and then returns to the user the leads that have posted/commented about their problem'"""
test = stage_1_end_user_description(product_description)


def stage_2_keyword_generation(users) : 
    llm = OpenAI()
    prompt = """ based on these target customer types, Give 3 keywords for each customer type to serach on reddit for relevant communities. For each user input in the JSON given, you are to add a new field called 'keywords' structured like this : 
    "keywords" : [{keyword 1}, {keyword 2}, etc]: 
    here is the JSON you will add to : """ 
    temp = 1 
    users_json_with_keywords = llm.open_ai_gpt4_turbo_call(users, prompt, temp)
    return users_json_with_keywords

test2 = stage_2_keyword_generation(test)
print(test2)