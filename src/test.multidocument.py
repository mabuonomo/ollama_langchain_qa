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

ollama_url = os.getenv("OLLAMA_URL", "http://ollama_chat:11434")
ollama_model = os.getenv("OLLAMA_MODEL", "mistral")
vectordb_path = os.getenv("VECTORDB_PATH", ".data")
ollama_obj = Ollama(base_url=ollama_url, model=ollama_model)
ollama_embeddings = OllamaEmbeddings(base_url=ollama_url, model=ollama_model)

print(f"Using Ollama at {ollama_url} with model {ollama_model}")

documents = []
for file in os.listdir('src/docs'):
    if file.endswith('.pdf'):
        pdf_path = './src/docs/' + file
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        doc_path = './src/docs/' + file
        loader = Docx2txtLoader(doc_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        text_path = './src/docs/' + file
        loader = TextLoader(text_path)
        documents.extend(loader.load())

# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunked_documents = text_splitter.split_documents(documents)

print(f"Loaded {len(documents)} documents")

vectordb = Chroma.from_documents(
    documents, 
    embedding=ollama_embeddings, 
    persist_directory=vectordb_path)
vectordb.persist()

print(f"Created vectorstore")

# pdf_qa = ConversationalRetrievalChain.from_llm(
#     ollama_obj,
#     vectordb.as_retriever(search_kwargs={'k': 6}),
#     return_source_documents=True,
#     verbose=True
# )

qachain=RetrievalQA.from_chain_type(ollama_obj, retriever=vectordb.as_retriever())

print(f"Created QA chain")

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"

# chat_history = []
print(f"{yellow}---------------------------------------------------------------------------------")
print('Welcome to the DocBot. You are now ready to start interacting with your documents')
print('---------------------------------------------------------------------------------')
while True:
    query = input(f"{green}Prompt: ")
    if query == "exit" or query == "quit" or query == "q" or query == "f":
        print('Exiting')
        sys.exit()
    if query == '':
        print('Query cannot be empty. Please enter a valid query.')
        continue
    # result = pdf_qa(
    #     {
    #         "question": query, 
    #         "chat_history": chat_history
    #     }
    # )

    result = qachain({"query": query})

    print(f"{white}Answer: " + result["answer"])
    # chat_history.append((query, result["answer"]))