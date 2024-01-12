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

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)

vectordb = Chroma.from_documents(documents, embedding=
    OllamaEmbeddings(
        base_url="http://cowtechgo_chat_ollama:11434",
        model="mistral"
    ), 
    persist_directory="./data")
vectordb.persist()

pdf_qa = ConversationalRetrievalChain.from_llm(
    Ollama(
        base_url="http://cowtechgo_chat_ollama:11434",
        model="mistral"
        ),
    vectordb.as_retriever(search_kwargs={'k': 6}),
    return_source_documents=True,
    verbose=False
)

yellow = "\033[0;33m"
green = "\033[0;32m"
white = "\033[0;39m"

chat_history = []
print(f"{yellow}---------------------------------------------------------------------------------")
print('Welcome to the DocBot. You are now ready to start interacting with your documents')
print('---------------------------------------------------------------------------------')
while True:
    query = input(f"{green}Prompt: ")
    if query == "exit" or query == "quit" or query == "q" or query == "f":
        print('Exiting')
        sys.exit()
    if query == '':
        continue
    result = pdf_qa(
        {"question": query, "chat_history": chat_history})
    print(f"{white}Answer: " + result["answer"])
    chat_history.append((query, result["answer"]))