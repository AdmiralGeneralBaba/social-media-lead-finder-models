from openai import OpenAI, AsyncOpenAI
from pinecone import Pinecone, ServerlessSpec
import asyncio
import math


pc = Pinecone(api_key='b726d64c-a756-4aca-a368-a5b31f1f76a6')



client = OpenAI()
async_client = AsyncOpenAI()
test = [{'id': 't3_1aloclp', 'parsedId': '1aloclp', 'url': 'https://www.reddit.com/r/digital_marketing/comments/1aloclp/tips_for_marketing_of_new_podcast/', 'username': 'LuckyFall6205', 'title': 'Tips for Marketing of New Podcast', 'communityName': 'r/digital_marketing', 'parsedCommunityName': 'digital_marketing', 'body': "I met a senior journalist at a B2B meeting, introduced by my dad. He's a script writer and content creator for documentaries, aged 62, seeking advice on better podcast marketing. \n\nI suggested using Spotify Advertising Manager, Google Ads, Meta Ads, etc. \n\nDespite being new to podcast marketing and more focused on content design and media buying, I felt a bit out of my element. Any additional tips would be appreciated!\n\nThe topic of podcast is [The focus on issues relevant to people's lives and society as a whole]", 'html': '&lt;!-- SC_OFF --&gt;&lt;div class="md"&gt;&lt;p&gt;I met a senior journalist at a B2B meeting, introduced by my dad. He&amp;#39;s a script writer and content creator for documentaries, aged 62, seeking advice on better podcast marketing. &lt;/p&gt;\n\n&lt;p&gt;I suggested using Spotify Advertising Manager, Google Ads, Meta Ads, etc. &lt;/p&gt;\n\n&lt;p&gt;Despite being new to podcast marketing and more focused on content design and media buying, I felt a bit out of my element. Any additional tips would be appreciated!&lt;/p&gt;\n\n&lt;p&gt;The topic of podcast is [The focus on issues relevant to people&amp;#39;s lives and society as a whole]&lt;/p&gt;\n&lt;/div&gt;&lt;!-- SC_ON --&gt;', 'numberOfComments': 2, 'flair': 'Discussion', 'upVotes': 0, 'isVideo': False, 'isAd': False, 'over18': False, 'createdAt': '2024-02-08T05:29:48.000Z', 'scrapedAt': '2024-02-12T20:40:28.124Z', 'dataType': 'post'}]


#method to get and return embedding for the inputted text
def get_embedding(text, model="text-embedding-3-small") : 
    text = text.replace("\n", " ")
    embedding = client.embeddings.create(input= [text], model=model).data[0].embedding
    return embedding

async def async_get_embedding(text, model="text-embedding-3-small") : 
    text = text.replace("\n", " ")
    estimated_token_limit = 5800
    if len(text) > estimated_token_limit: 
        text = text[:estimated_token_limit]
    embedding = await async_client.embeddings.create(input=[text], model=model)
    embedding_return = embedding.data[0].embedding
    return embedding_return

def query_pinecone_vector_database(index, vectors, top_k) : 
    index = pc.Index(index)
    query_results = index.query( 
        vector=vectors,
        top_k=top_k,
        include_values=False
    )   
    return query_results 

#Calls embedding functio nfor each of the jsons within the JSON array
def add_embedding_post_json(process_post_json) :
    print(process_post_json)
    for post_json in process_post_json : 
        post_json_embedding = get_embedding(post_json['content'])
        print("added embedding for ")
        post_json['values'] = post_json_embedding
    return process_post_json

async def async_add_embedding_post_json(process_post_json) :
    print(process_post_json)
    embeddings_array = []
    tasks = [async_get_embedding(post_json['content']) for post_json in process_post_json]
    print("Generating embeddings for JSON content values...")
    embeddings_array = await asyncio.gather(*tasks)
     
    for post_json, embedding in zip(process_post_json, embeddings_array) : 
        post_json['values'] = embedding

    return process_post_json
#upserts the proccessed post json with the vlaues of the vectors iwtihin it into the pinecone index database. Have this, in the future, relate to the user's ID so that everything they have scrapped is kept within the vector 
# database as a store (or perhaps in the far futrue have it so that ALL reddit subreddits are crawled and updated on a mass scale, but that is for another time.)

def create_pinecone_index_post_json(processed_post_json, index_name) : 
    if index_name not in pc.list_indexes().names():
    # Do something, such as create the index
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric='cosine',
            spec=ServerlessSpec(
            cloud="aws",
            region="us-west-2"
            )
        )

    index = pc.Index(index_name)
    vectors = []
    for json in processed_post_json :  
        #Adds in all of the information relating to the post to the pinecone database, within the metadata : 
        vectors.append({
                "id": json['id'],
                "values": json['values'],
                "metadata": {
                    "username": json['username'],
                    "userId": json['userId'],
                    "url": json['url'],
                    "content": json['content'],
                    "communityName": json['communityName'],
                    "parsedCommunityName": json['parsedCommunityName'],
                    "numberOfComments": json['numberOfComments'],
                    "upVotes": json['upVotes'],
                    "isVideo": json['isVideo'],
                    "isAd": json['isAd'],
                    "over18": json['over18'],
                    "createdAt": json['createdAt'],
                    "scrapedAt": json['scrapedAt'],
                    "dataType": json['dataType']
                }
                })
        
    index.upsert(
        vectors=vectors
    )
    return index_name

def embed_and_upsert_to_pinecone(raw_post_json, index) : 
    # half_processed_post_json = process_post_json(raw_post_json)
    print("Creating embeddings...")
    fully_processed_json = add_embedding_post_json(raw_post_json)
    print("Embeddings added! adding to pinecone...")
    pinecone_vd = create_pinecone_index_post_json(fully_processed_json, index)
    print("Added to pinecone!")
    return pinecone_vd

async def async_embed_and_upsert_to_pinecone(raw_post_json, index) : 
    # half_processed_post_json = process_post_json(raw_post_json)
    print("Creating embeddings...")
    fully_processed_json = await async_add_embedding_post_json(raw_post_json)
    print("Embeddings added! adding to pinecone...")
    print("This is the length of the json :", len(fully_processed_json))
    chunk_size = 150
    for i in range(0, len(fully_processed_json), chunk_size):
        # Create a chunk by slicing the fully_processed_json
        json_chunk = fully_processed_json[i:i+chunk_size]
        
        # Process each chunk as needed (e.g., add to Pinecone)
        pinecone_vd = create_pinecone_index_post_json(json_chunk, index)
        print(f"Chunk {i//chunk_size + 1} added to Pinecone!")
    print("Added to pinecone!")
    return pinecone_vd

def query_fetch_id_information(id_set, index) : 
    index = pc.Index(index)
    id_information = []
    id_list = list(id_set)
    index_results = index.fetch(ids=id_list)
    for key in index_results['vectors']: 
        index_result = index_results['vectors'][key]
        id_information.append(index_result)
    return id_information

# embed_and_upsert_to_pinecone(test_dictionary)
# input_vectors = get_embedding("""My Jet rental business is made up of 2 bombardier challenger 601-3A which we rent at £5000 per hour and 4 hawker 900xp rented at £6400 or the country's currency equivalent like I think it's over 7k euros in Spai.  my customers are people who wish to travel in style and comfort and without the hassles of regular commercial air travel 
# Usually top business execs and popular celebrities""")
# print(query_pinecone_vector_database("test-index", input_vectors, 15))


# test_index = "test-index"

# index = pc.Index(test_index)

test_json = [{
  "id": "t3_1ave16e",
  "parsedId": "1ave16e",
  "url": "https://www.reddit.com/r/LuxuryTravel/comments/1ave16e/luxury_accommodation_scams_how_to_detect_them/",
  "username": "ah_blogs",
  "userId": "t2_u5ojcq4i",
  "content": "Luxury accommodation scams: how to detect them before booking online - travel tips - expert traveller",
  "communityName": "r/LuxuryTravel",
  "parsedCommunityName": "LuxuryTravel",
  "body": "URL: https://airportsandhotelsblog.wordpress.com/2023/11/13/accommodation-scams-how-to-detect-them-before-booking-online/\n",
  "html": None,
  "numberOfComments": 0,
  "flair": None,
  "upVotes": 1,
  "isVideo": False,
  "isAd": False,
  "over18": False,
  "createdAt": "2024-02-20T09:55:12.000Z",
  "scrapedAt": "2024-02-22T12:55:11.069Z",
  "dataType": "post"
},
{
  "id": "t3_1av72nv",
  "parsedId": "1av72nv",
  "url": "https://www.reddit.com/r/LuxuryTravel/comments/1av72nv/share_your_blissful_moments_at_sapphire_shores/",
  "username": "cC_cReation_HouSe",
  "userId": "t2_l159g6ha",
  "content": "Share Your Blissful Moments at Sapphire Shores Luxury Retreat in Destin, FL! 🏝️✨",
  "communityName": "r/LuxuryTravel",
  "parsedCommunityName": "LuxuryTravel",
  "body": "URL: https://mirageproperties.com/\n",
  "html": None,
  "numberOfComments": 0,
  "flair": None,
  "upVotes": 1,
  "isVideo": False,
  "isAd": False,
  "over18": False,
  "createdAt": "2024-02-20T03:00:56.000Z",
  "scrapedAt": "2024-02-22T12:55:11.283Z",
  "dataType": "post"
}]

asyncio.run(async_embed_and_upsert_to_pinecone(test_json, index='test-index'))
# id_list = ['t3_1aq38xe', 't3_1aqlq57','t3_1ard7c5']