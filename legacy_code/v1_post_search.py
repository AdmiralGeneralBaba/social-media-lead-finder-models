from openai_calls import OpenAI
import re


def evaluate_post(problem, post_body) : 
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
   

def v1_post_serach(scraped_posts, problem) : 
    diluted_posts = []
    for post in scraped_posts : 
        input_post_body = post['body']
        result = evaluate_post(problem, input_post_body)
        if result == True : 
            diluted_posts.append(post)
    return diluted_posts