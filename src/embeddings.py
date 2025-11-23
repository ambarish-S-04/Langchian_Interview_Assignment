import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

def compute_embeddings():
    load_dotenv('api.env')
    
    if not os.getenv("MISTRAL_API_KEY"):
        raise ValueError("MISTRAL_API_KEY environment variable not set")
    
    data_dir = Path("Data")
    persist_directory = "vectorstore"
    
    data_dir.mkdir(parents=True, exist_ok=True)
    
    embeddings = MistralAIEmbeddings(
        model="mistral-embed",
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )
    loader = DirectoryLoader(str(data_dir), glob="*.txt", loader_cls=TextLoader, show_progress=True, loader_kwargs={'encoding': 'utf-8'})
    
    documents = loader.load()
    
    if not documents:
        print(f"No .txt story files found in {data_dir}. Please add some .txt files there first.")
        return
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(documents)
    
    vectordb = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    # Persist the database
    vectordb.persist()
    print(f"Embeddings computed and stored in {persist_directory}")