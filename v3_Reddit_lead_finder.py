from v1_subreddits_finder import stage_3_final
from v1_subreddit_scanner import stage_4_scrape_posts
from v2_post_search import v2_post_search
from embedding_module import async_embed_and_upsert_to_pinecone
from test_json import test_dictionary
import asyncio


# This combines all of the other methods of the V3 reddit lead finder. Scrapes subreddits, uses GPT to analyse them, then returns the leads that match.
# This the is JSON array output structure : 

#[
#{
#"id" : {value}
#"values" : {numbers}
#"metadata" : {"username" : {username_of_user}, "content" : {content}, "url" : {url} }
#}
#]

#await this endpoint.
async def v3_reddit_lead_finder(product_description, user_id_index_name) : 
    print("Starting lead finder...")
    print("Generating the URL array.")
    url_array = await stage_3_final(product_description=product_description)
    print("Created the URL array...")
    # scraped_posts = await stage_4_scrape_posts(url_array)
    print("Scraped posts, added them to pinecone...")
    await async_embed_and_upsert_to_pinecone(test_dictionary, user_id_index_name)
    print("Searching the posts...")
    final_leads = await v2_post_search(product_description, user_id_index_name)
    return final_leads






####################################### TESTING CODE ############################################



test_product_description = """ 'Our company creates viral content using AI, to create a organic following and demand, platforms like instagram and tiktok' """
test_user_id = "test-index"
test_output = asyncio.run(v3_reddit_lead_finder(test_product_description, test_user_id))

# print(len(test_output))
# print(test_output[0]['metadata']['content'])