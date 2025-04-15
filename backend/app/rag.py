from langchain_community.llms import ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader ,WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os 
import random 

#importing the ollama library
llms = ollama.Ollama(model="llama2", temperature=0.1)
embeddings = OllamaEmbeddings()

# setting up the vector store
PERSISTENCE_DIR = os.getenv("PERSISTENCE_DIR", "./chroma_db")
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=PERSISTENCE_DIR,
)

# text splitter for splitting documents into smaller chunks
# for better processing
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# function to ingest documents into the vector store
def ingest_document(file_path: str, user_id: int ,file_type : str = "pdf"):
      if file_type == "pdf":
          loader = PyPDFLoader(file_path)
      elif file_type == "web":
          loader = WebBaseLoader(file_path)
      else:
          raise ValueError("Unsupported file type")
      documents = loader.load()
      splits = text_splitter.split_documents(documents)
      for split in splits:
          split.metadata["user_id"] = user_id
      vectorstore.add_documents(splits)
      
# replace similarity search by vector with the one that filters by user_id
def answer_question(question: str, user_id: int):
      question_embedding = embeddings.embed_query(question)
      
      docs = vectorstore.similarity_search_by_vector(
          question_embedding, k=5, filter={"user_id": user_id}
      )
      context = "\n".join([doc.page_content for doc in docs])
      prompt = (
          f"based on the following context, answer the question:\n\n {context}\n\n"
          f"followed by a detailed explanation :\n\n {context}\n\n"
      )
      
      response = llms(prompt)
      
      #calculating the tokens used (approximate)
      # this is an approximation and may not be accurate
      tokens_used = llms.get_tokens_used()
       
      if not docs:
          return "No relevant documents found."
      random_doc = random.choice(docs)
        
   
