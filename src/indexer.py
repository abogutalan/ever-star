import os
from elasticsearch import Elasticsearch
from langchain_community.document_loaders import BSHTMLLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import ElasticVectorSearch
from data.Search.indexer_of_search import Indexer
from data.Search.scraper_of_search import SparkNLPScraper


from config import Paths, openai_api_key

import argparse
import sys

from data.Search.semantic_search_service import SemanticSearchService

def run_scraper_of_search(file_name):
    scraper = SparkNLPScraper() # can pass in a url here
    scraper.scrape_website()
    scraper.to_csv(file_name)

def search():
    # Set up OpenAI API key and Elasticsearch client
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Check if the API key is present
    if not openai_api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it before running the script.")
    
    # Create an instance of the Elasticsearch client
    es_client = Elasticsearch(hosts=["http://localhost:9200"])

    # Create an instance of the semantic search service class
    semantic_search_service = SemanticSearchService(openai_api_key, es_client)

    # Create an instance of the Indexer class
    indexer = Indexer(es_client, semantic_search_service.get_embedding)

    # Load (and index if necessary) the data
    index_name = "sample"
    file_name = 'data/Search/search_data.csv'

    # scrape the data and write to search_data.csv
    run_scraper_of_search(file_name)

    # delete index if exists
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)

    indexer.load_index(file_name, index_name)

def ask(path, index_name):
    
    loader = BSHTMLLoader(str(path))
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    documents = text_splitter.split_documents(data)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = ElasticVectorSearch.from_documents(
        documents,
        embeddings,
        elasticsearch_url="http://localhost:9200",
        index_name=index_name,
        # request_timeout=600,

    )
    print(db.client.info())

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Process command-line arguments. Use "ask_documents", "ask_models" or "search" after the filename. Example: python index.py ask_documents')

    # Add the arguments
    parser.add_argument('Cmd', metavar='cmd', type=str, help='the command to run')

    # If no arguments were passed, print help message and return
    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        return

    # Parse the arguments
    args = parser.parse_args()

    if args.Cmd == 'ask_documents':
        ask(Paths.documents, "documents-index")
    elif args.Cmd == 'ask_models':
        # Indexing models takes 242.7 second(s)
        ask(Paths.models, "models-index")
    elif args.Cmd == 'search':
        search()
    else:
        print(f'Unknown command {args.Cmd}')

if __name__ == "__main__":
    main()
