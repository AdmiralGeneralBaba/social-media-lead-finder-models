from openai_calls import OpenAI
import asyncio
import json

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


###############   example usage down here  ######################
product_description = """ 'My startup aims to allow users to type in the problem that their product is supposed to solve, and then from this it searches multiple social media platforms and then returns to the user the leads that have posted/commented about their problem'"""
test = stage_1_end_user_description(product_description)
print(test)


