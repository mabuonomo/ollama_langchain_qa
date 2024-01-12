# https://github.com/jmorganca/ollama/blob/main/docs/tutorials/langchainpy.md

import os
import sys

from langchain.document_loaders import PyPDFLoader
from langchain.llms import Ollama
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import JSONLoader

ollama_url = os.getenv("OLLAMA_URL", "http://ollama_chat:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "mistral")
vectordb_path = os.getenv("VECTORDB_PATH", ".data")
ollama_obj = Ollama(base_url=ollama_url, model=ollama_model)
ollama_embeddings = OllamaEmbeddings(base_url=ollama_url, model=ollama_model)
docs_dir = os.getenv("DOCS_DIR", "./src/docs")

print(f"Using Ollama at {ollama_url} with model {ollama_model}")

documents = []
for file in os.listdir(docs_dir):
    file_path = os.path.join(docs_dir, file)

    if file.endswith('.json'):
        loader = JSONLoader(file_path)
        documents.extend(loader.load())
    if file.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        loader = Docx2txtLoader(file_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        loader = TextLoader(file_path)
        documents.extend(loader.load())

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
chunked_documents = text_splitter.split_documents(documents)

print(f"Loaded {len(documents)} documents")

vectordb = Chroma.from_documents(
    documents, 
    embedding=ollama_embeddings, 
    persist_directory=vectordb_path)
vectordb.persist()

print(f"Created vectorstore")

qachain=RetrievalQA.from_chain_type(ollama_obj, retriever=vectordb.as_retriever())

print(f"Created QA chain")

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"

print(f"{yellow}---------------------------------------------------------------------------------")
print('Welcome to the OllamaBot! Ask me a question about the documents in the docs folder.')
print('---------------------------------------------------------------------------------')
while True:
    query = input(f"{green}Prompt: ")
    if query == "exit" or query == "quit" or query == "q" or query == "f":
        print('Exiting')
        sys.exit()
    if query == '':
        print('Query cannot be empty. Please enter a valid query.')
        continue
    result = qachain({"query": query})

    print(f"{white}Answer: " + result["result"])
