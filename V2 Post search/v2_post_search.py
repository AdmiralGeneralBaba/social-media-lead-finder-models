import embedding_module as e

test = "test"

vectors = e.get_embedding(test) 
print(vectors)
test = e.query_pinecone_vector_database(index="test-index",vectors=vectors, top_k=1)

print(test)
 