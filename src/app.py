import os
import elasticsearch
from fastapi import FastAPI
from config import openai_api_key
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_community.vectorstores import ElasticVectorSearch
from data.Search.semantic_search_service import SemanticSearchService

if not openai_api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it before running the script.")

embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

def create_qa(index_name):
    db = ElasticVectorSearch(
    elasticsearch_url="http://localhost:9200",
    index_name=index_name,
    embedding=embedding,
    )

    qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=db.as_retriever(),
    )

    return qa

qa_documents = create_qa("documents-index")
qa_models = create_qa("models-index")

# Create an instance of the Elasticsearch client
es_client = elasticsearch.Elasticsearch(hosts=["http://localhost:9200"])
# Create an instance of the semantic search service class
semantic_search_service = SemanticSearchService(openai_api_key, es_client)

app = FastAPI()

@app.get("/")
def index():
    return {
        "message": "Make a post request to /ask to ask questions about Document"
    }

@app.post("/ask_documents")
def ask(query: str):
    response = qa_documents.run(query)
    return {
        "response": response,
    }

@app.post("/ask_models")
def ask(query: str):
    response = qa_models.run(query)
    # response = "hardcode to test so that OpenAI does not charge!"
    return {
        "response": response,
    }

@app.post("/search")
def search(query: str):
    results = semantic_search_service.semantic_search(query, index_name="sample", top_k=5)
    return {
        "results": results,
    }
