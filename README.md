# Semantic search with Elasticsearch, OpenAI, and LangChain

### Project Name: Semantic Scholar: An Advanced Semantic Search Engine

### Description:

Designed an advanced semantic search engine called "Semantic Scholar" leveraging Elasticsearch, OpenAI's Language Model (GPT), LangChain, and FastAPI. This robust engine provides the ability to interact with large volumes of text and answer complex queries by extracting the most relevant content.

Implemented using Elasticsearch, a popular search and analytics engine, it indexes data and responds to complex queries at rapid speeds. OpenAI's Language Model (GPT) was utilized for its capacity to understand and generate human-like text. LangChain, a library specifically designed for interaction with Large Language Models (LLMs), was deployed to handle routine tasks such as text extraction and indexing. FastAPI, a modern and fast web framework, was used for building the APIs.

This project showcases a practical implementation of semantic search, demonstrating effective data indexing, information retrieval, and relevance mapping using cutting-edge technologies.

Technologies: Python, Elasticsearch, OpenAI GPT, LangChain, FastAPI.

### How to run:
```
cd src/
python indexer.py search
python indexer.py ask_documents
python indexer.py ask_models
uvicorn app:app --reload
http://127.0.0.1:8000/docs
```

search:
How to convert token to chunk?

ask_documents:
what is BartTransformer?

ask_model:
How to extract medications and resolve their adverse reactions?




##### Resources

[Spark NLP - Quick Start](https://sparknlp.org/docs/en/quickstart).
[How I Turned My Company’s Docs into a Searchable Database with OpenAI](https://towardsdatascience.com/how-i-turned-my-companys-docs-into-a-searchable-database-with-openai-4f2d34bd8736#34d3).
[Semantic search with Elasticsearch, OpenAI, and LangChain](https://dylancastillo.co/semantic-search-elasticsearch-openai-langchain/).


Repoya eklenecek
data science and software ekibi var
code base i anla
bizim tarafi oraya entegre edicez
software ekibinin yazdigi kodu anlamak
LLM fine tune etme
GPU servera baglanip LLM fine tune etme
back end sessions
restapi container vs
langchain anlatma olabilir
