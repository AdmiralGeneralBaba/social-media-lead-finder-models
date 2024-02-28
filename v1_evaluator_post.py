import datetime
import asyncio
from datetime import datetime
from test_json import test_dictionary
from openai_calls import OpenAI
import re


######### THESE ARE THE LLM EVAL CALLS  : #######


# Each one of these evaluates the post. Change the prompt for each category to change the evaluation strictness.
async def category_1_post_evaluation(problem, content) : 
    llm = OpenAI()
    prompt = """   You are an expert lead validator, who has decades of experience in being able to identify whether or not a lead has potential interest in a company.

Provided to you will be two things, 1. a description of the problem that a company solves, and 2. a post from a reddit user that has been marked as possibly a target lead with this problem.

Your job is evaluate this post, and make a decision on whether or not it is a potential lead. 

When you have made up your mind, type either 'YES' or 'NO' at the end. 

Here is the problem the company is solving : + """ + f"{problem}" + """w

and here is the reddit post :

Be harsh in your judgement, this person MUST relate completely to the problem at hand or you will be fired.
Lets think step by step to get the right answer."""
    temp = 0.9
    result = await llm.async_open_ai_gpt4_call(content, prompt, temp)
    yes_finder = r"(YES)"
    find_results = re.findall(yes_finder, result)
    if find_results :
        return True
    return False
async def category_2_post_evaluation(problem, content) : 
    llm = OpenAI()
    prompt = """   You are an expert lead validator, who has decades of experience in being able to identify whether or not a lead has potential interest in a company.

Provided to you will be two things, 1. a description of the problem that a company solves, and 2. a post from a reddit user that has been marked as possibly a target lead with this problem.

Your job is evaluate this post, and make a decision on whether or not it is a potential lead. 

When you have made up your mind, type either 'YES' or 'NO' at the end. 

Here is the problem the company is solving : + """ + f"{problem}" + """w

and here is the reddit post :

Make sure your judgement is correct. IF YOU DONT YOU WILL BE FIRED AND THE COMPANY WILL FAIL
Lets think step by step to get to the right answer. """
    temp = 0.9
    result = await llm.async_open_ai_gpt4_call(content, prompt, temp)
    yes_finder = r"(YES)"
    find_results = re.findall(yes_finder, result)
    if find_results :
        return True
    return False
async def category_3_post_evaluation(problem, content) : 
    llm = OpenAI()
    prompt = """   You are an expert lead validator, who has decades of experience in being able to identify whether or not a lead has potential interest in a company.

Provided to you will be two things, 1. a description of the problem that a company solves, and 2. a post from a reddit user that has been marked as possibly a target lead with this problem.

Your job is evaluate this post, and make a decision on whether or not it is a potential lead. 

When you have made up your mind, type either 'YES' or 'NO' at the end. 

Here is the problem the company is solving : + """ + f"{problem}" + """w

and here is the reddit post :

Make sure your judgement is correct. IF YOU DONT YOU WILL BE FIRED AND THE COMPANY WILL FAIL
Lets think step by step to get to the right answer. """
    temp = 0.9
    result = await llm.async_open_ai_gpt4_call(content, prompt, temp)
    yes_finder = r"(YES)"
    find_results = re.findall(yes_finder, result)
    if find_results :
        return True
    return False
async def category_4_post_evaluation(problem, content) : 
    llm = OpenAI()
    prompt = """   You are an expert lead validator, who has decades of experience in being able to identify whether or not a lead has potential interest in a company.

Provided to you will be two things, 1. a description of the problem that a company solves, and 2. a post from a reddit user that has been marked as possibly a target lead with this problem.

Your job is evaluate this post, and make a decision on whether or not it is a potential lead. 

When you have made up your mind, type either 'YES' or 'NO' at the end. 

Here is the problem the company is solving : + """ + f"{problem}" + """w

and here is the reddit post :

Make sure your judgement is correct. IF YOU DONT YOU WILL BE FIRED AND THE COMPANY WILL FAIL
Lets think step by step to get to the right answer. """
    temp = 0.9
    result = await llm.async_open_ai_gpt4_call(content, prompt, temp)
    yes_finder = r"(YES)"
    find_results = re.findall(yes_finder, result)
    if find_results :
        return True
    return False

# Takes in a lsit of scrapped JSON objects, then organises the leads based on how recent htey are to the current time
def organise_k_results( combined_retrieved_posts) : 
    # Calculates the time difference between the post date and the current date : 
    def calculate_time_difference(createdAt) : 
        created_at_datetime = datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_time = datetime.now()
        time_difference = current_time - created_at_datetime
        time_difference = time_difference.days
        return time_difference
    # Each category here denotes how 'hot' a lead is (category 1 being the earliest, category 2 less recent, etc)
    json = {}
    category_1 = []
    category_2 = []
    category_3 = []
    category_4 = []
    for post in combined_retrieved_posts : 
        post_time_difference = calculate_time_difference(post['metadata']['createdAt'])
        if post_time_difference <= 5 :
            category_1.append(post)
        elif 5 < post_time_difference <= 30 : 
            category_2.append(post)
        elif 30 < post_time_difference <= 180: 
            category_3.append(post)
        elif 180 < post_time_difference : 
            category_4.append(post)
    json['category_1'] = category_1
    json['category_2'] = category_2
    json['category_3'] = category_3
    json['category_4'] = category_4
    return json

def v1_evaluator_post(problem : str, returned_k_results) : 
    evaluation_tasks = []
    organised_k_results = organise_k_results(returned_k_results)
    for k_result in organised_k_results['category_1'] : 
        evaluation_tasks.append(category_1_post_evaluation(problem, k_result['metadata']['content']))
    for k_result in organised_k_results['category_2'] : 
        evaluation_tasks.append(category_2_post_evaluation(problem, k_result['metadata']['content']))
    for k_result in organised_k_results['category_3'] : 
        evaluation_tasks.append(category_3_post_evaluation(problem, k_result['metadata']['content']))
    for k_result in organised_k_results['category_4'] : 
        evaluation_tasks.append(category_4_post_evaluation(problem, k_result['metadata']['content']))
    return evaluation_tasks

def v2_evaluator_post(problem : str, returned_k_results) : 
    evaluation_tasks = []
    for k_result in returned_k_results : 
        evaluation_tasks.append(category_1_post_evaluation(problem, k_result['metadata']['content']))
    return evaluation_tasks