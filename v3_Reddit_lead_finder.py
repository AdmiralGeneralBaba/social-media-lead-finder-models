from v1_subreddits_finder import stage_3_final
from v1_subreddit_scanner import stage_4_scrape_posts
from V2_post_search.v2_post_search import v2_post_search
from V2_post_search.embedding_module import async_embed_and_upsert_to_pinecone
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

async def v3_reddit_lead_finder(product_description, user_id_index_name) : 
    url_array = stage_3_final(product_description=product_description)
    scraped_posts = stage_4_scrape_posts(url_array)
    await async_embed_and_upsert_to_pinecone(scraped_posts, user_id_index_name)
    final_leads = v2_post_search(product_description, user_id_index_name)
    return final_leads


# test_product_description = """ 'Our company creates viral content using AI, to create a organic following and demand, platforms like instagram and tikto' """
# test_user_id = "test-index"
# v3_reddit_lead_finder(test_product_description, test_user_id)