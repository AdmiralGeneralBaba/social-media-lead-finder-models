from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key='b726d64c-a756-4aca-a368-a5b31f1f76a6')



client = OpenAI()

test = [{'id': 't3_1aloclp', 'parsedId': '1aloclp', 'url': 'https://www.reddit.com/r/digital_marketing/comments/1aloclp/tips_for_marketing_of_new_podcast/', 'username': 'LuckyFall6205', 'title': 'Tips for Marketing of New Podcast', 'communityName': 'r/digital_marketing', 'parsedCommunityName': 'digital_marketing', 'body': "I met a senior journalist at a B2B meeting, introduced by my dad. He's a script writer and content creator for documentaries, aged 62, seeking advice on better podcast marketing. \n\nI suggested using Spotify Advertising Manager, Google Ads, Meta Ads, etc. \n\nDespite being new to podcast marketing and more focused on content design and media buying, I felt a bit out of my element. Any additional tips would be appreciated!\n\nThe topic of podcast is [The focus on issues relevant to people's lives and society as a whole]", 'html': '&lt;!-- SC_OFF --&gt;&lt;div class="md"&gt;&lt;p&gt;I met a senior journalist at a B2B meeting, introduced by my dad. He&amp;#39;s a script writer and content creator for documentaries, aged 62, seeking advice on better podcast marketing. &lt;/p&gt;\n\n&lt;p&gt;I suggested using Spotify Advertising Manager, Google Ads, Meta Ads, etc. &lt;/p&gt;\n\n&lt;p&gt;Despite being new to podcast marketing and more focused on content design and media buying, I felt a bit out of my element. Any additional tips would be appreciated!&lt;/p&gt;\n\n&lt;p&gt;The topic of podcast is [The focus on issues relevant to people&amp;#39;s lives and society as a whole]&lt;/p&gt;\n&lt;/div&gt;&lt;!-- SC_ON --&gt;', 'numberOfComments': 2, 'flair': 'Discussion', 'upVotes': 0, 'isVideo': False, 'isAd': False, 'over18': False, 'createdAt': '2024-02-08T05:29:48.000Z', 'scrapedAt': '2024-02-12T20:40:28.124Z', 'dataType': 'post'}]
  
# This includes only ythe needed values in the new JSON to make it less confusing 
def process_post_json(jsons) : 
    new_jsons = []

    for json in jsons : 
        print(json)
        content = json['title'] + " " + json['body']
        new_json = {'id' : json['id'], 'content' : content, 'username' : json['username'], 'url' : json['url']}
        new_jsons.append(new_json)
    return new_jsons

#method to get and return embedding for the inputted text
def get_embedding(text, model="text-embedding-3-small") : 
    text = text.replace("\n", " ")
    embedding = client.embeddings.create(input= [text], model=model).data[0].embedding
    return embedding

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
        post_json['values'] = post_json_embedding
    return process_post_json

#upserts the proccessed post json with the vlaues of the vectors iwtihin it into the pinecone index database. Have this, in the future, relate to the user's ID so that everything they have scrapped is kept within the vector 
# database as a store (or perhaps in the far futrue have it so that ALL reddit subreddits are crawled and updated on a mass scale, but that is for another time.)

def create_pinecone_index_post_json(processed_post_json) : 
    index_name = "test-index"
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
        vectors.append( {"id" : json['id'], "values" : json['values'],
             "metadata" : {"username" : json['username'], "content" : json['content'], "url" : json['url']}})
        
    index.upsert(
        vectors=vectors
    )
    return index_name

def embed_and_upsert_to_pinecone(post_json) : 
    half_processed_post_json = process_post_json(post_json)
    print("Creating embeddings...")
    fully_processed_json = add_embedding_post_json(half_processed_post_json)
    print("Embeddings added! adding to pinecone...")
    pinecone_vd = create_pinecone_index_post_json(fully_processed_json)
    print("Added to pinecone!")
    return pinecone_vd


input_vectors = get_embedding("struggling to advertise properly")
print(query_pinecone_vector_database("test-index", input_vectors, 5))