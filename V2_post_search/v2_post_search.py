import V2_post_search.embedding_module as e
from V2_post_search.test_dictionary import text_dictionary
from openai_calls import OpenAI
import re
import json



def vd_search_queries(problem) : 
    llm = OpenAI()
    temp = 0.9
    prompt = """ Given to you will be a problem that a company solves. Your job is to give different ways of saying this problem, such that the semantic meaning is the same but it explores different search spaces in the context of retrieving the maximum amount of relevant results from a search.
Your search queries should go broader and more creative in their solution space, such that the final value you give in the array should be a search term that goes just on the edge of being an irrelevant search.
Think deeply about what the problem might link to, and then perform that search. For example, if the solution is about having fisherman catch more fish with a better hook, the last search term should be a broad problem about catching more fish in general.
The first 3 should be direct, the middle 3 should be roughly direct and the last 4 should be indirect.

In your output, you should ONLY give an array of text values. For example : 
[{search1here} {serach2here} etc]

Here is the problem  :
"""
    print("Generating search queries...")
    string_array_string = llm.open_ai_gpt4_call(problem, prompt, temp)
    search_array = json.loads(string_array_string)
    return search_array


# evaluates a post to see if it a good lead, return true if yes otherwise returns false.
def post_evaluation(problem, content) : 
    llm = OpenAI()
    prompt = """   You are an expert lead validator, who has decades of experience in being able to identify whether or not a lead has potential interest in a company.

Provided to you will be two things, 1. a description of the problem that a company solves, and 2. a post from a reddit user that has been marked as possibly a target lead with this problem.

Your job is evaluate this post, and make a decision on whether or not it is a potential lead. 

When you have made up your mind, type either 'YES' or 'NO' at the end. 

Here is the problem the company is solving : + """ + f"{problem}" + """

and here is the reddit post : 

Lets think step by step to get to the right answer. """
    temp = 0.9
    result = llm.open_ai_gpt4_call(content, prompt, temp)
    yes_finder = r"(YES)"
    find_results = re.findall(yes_finder, result)
    if find_results :
        return True
    return False



# retruns the distinct K elements from all of the search queries
def mulitple_query_vd(queries, index) : 
    vector_queries = []
    id_set = set()
    # This queries the VD with the search terms from the LLM.
    for query in queries : 
        print("generated embeddings for queries...")
        vector_queries.append(e.get_embedding(query))
    
    for vector in vector_queries : 
        similar_embeddings = e.query_pinecone_vector_database(index, vector, 10)
        for single_similar_embedding in similar_embeddings['matches']  : 
            if(single_similar_embedding['id'] not in id_set)  : 
               
                id_set.add(single_similar_embedding['id'])
    print("fetching id information...")
    returned_k_results = e.query_fetch_id_information(id_set, index)
            
    #Returns a list of the top K results for all of the queries types that are a distinct type
    return returned_k_results


# Evaluates each of the k results and returns the one that gave back true.
def evaluate_returned_k_results(problem : str, returned_k_results) : 
    evaluated_results = []
    print("Evaluating post leads...")
    for k_result in returned_k_results : 
        if (post_evaluation(problem, k_result['metadata']['content'])) == True : 
            evaluated_results.append(k_result)
            print(k_result['metadata']['content'])
    return evaluated_results


def v2_post_search(product_description, index) : 
   search_queries = vd_search_queries(product_description)
   returned_k_values = mulitple_query_vd(search_queries, index=index)
   print("Here are the number of returned k values : ", len(returned_k_values))
   final_leads =  evaluate_returned_k_results(product_description, returned_k_values)

   return final_leads


# test_product_description = """ 'My startup aims to allow users to type in the problem that their product is supposed to solve, and then from this it searches multiple social media platforms and then returns to the user the leads that have posted/commented about their problem'"""
# test_index = "test-index"
# final_leads = v2_post_search(test_product_description, test_index)
# print("these are the final leads : ")
# for i in range(len(final_leads)) :
#     print(len(final_leads))
#     print(final_leads[i]['id'])
 
# test = "test"
# print(len(test_dictionary))
# vector_database = e.embed_and_upsert_to_pinecone(test_dictionary)
# print(vector_database)

# id_set = ['t3_1aq38xe']
# test = e.query_fetch_id_information(id_set, 'test-index')
# print(test)