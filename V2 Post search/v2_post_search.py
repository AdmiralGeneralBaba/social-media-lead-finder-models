import embedding_module as e
from test_json import test_dictionary
from openai_calls import OpenAI
import re
import json


def vd_search_queries(problem) : 
    llm = OpenAI()
    temp = 1
    prompt = """ Given to you will be a problem that a company solves. Your job is to give different ways of saying this problem, such that the semantic meaning is the same but it explores different search spaces in the context of retrieving the maximum amount of relevant results from a search.
Your search queries should go broader and more creative in their solution space, such that the final value you give in the array should be a search term that goes just on the edge of being an irrelevant search.
Think deeply about what the problem might link to, and then perform that search. For example, if the solution is about having fisherman catch more fish with a better hook, the last search term should be a broad problem about catching more fish in general.
The first 3 should be direct, the middle 3 should be roughly direct and the last 4 should be indirect.

In your output, you should ONLY give an array of text values. For example : 
[{search1here} {serach2here} etc]

Here is the problem  :
"""
    string_array_string = llm.open_ai_gpt4_call(problem, prompt, temp)
    search_array = json.loads(string_array_string)
    return search_array


# evaluates a post to see if it a good lead, return true if yes otherwise returns false.
def post_evaluation(problem, content) : 
    llm = OpenAI()
    prompt = """   You are an expert lead validator, who has decades of experience in being able to identify whtehr or not a lead has postential interest in a company.

Provided to you will be two things, 1. a description of the problem that a company solves, and 2. a post from a reddit user that has been marked as possibly a target lead with this problem.

Your job is evaluate this post, and make a decision on whether or not it is a potential lead. 
=

When you have made up your mind, type either 'YES' or 'NO' at the end. 

Here is the problem the company is solving : + """ + f"{problem}" + """

and here is the reddit post : 

Lets think step by step to get to the right answer. """
    temp = 1
    result = llm.open_ai_gpt4_call(content, prompt, temp)
    yes_finder = r"(YES)"
    find_results = re.findall(yes_finder, result)
    if find_results :
        return True
    return False





# test = "test"
# print(len(test_dictionary))
# vector_database = e.embed_and_upsert_to_pinecone(test_dictionary)
# print(vector_database)