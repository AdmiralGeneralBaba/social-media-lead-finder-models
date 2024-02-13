import embedding_module as e
from test_json import test_dictionary
test = "test"
print(len(test_dictionary))
vector_database = e.embed_and_upsert_to_pinecone(test_dictionary)
print(vector_database)
