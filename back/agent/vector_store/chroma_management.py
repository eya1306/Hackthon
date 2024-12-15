import chromadb
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
load_dotenv()


client = chromadb.PersistentClient(path="./chroma_db")


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", api_key=os.getenv("GOOGLE_API_KEY"))




def collection_init(collection_name):
   """
   Initializes a collection in the vector store.

   Args:
      collection_name (str): Name of the collection to initialize or retrieve.

   Returns:
      Chroma: The initialized collection instance.
   """
   collection = Chroma(
      client=client,
      collection_name=collection_name,
      embedding_function=embeddings,
    )

   return collection


def add_new_doc(collection_name, message_id,message_text):
    """
    Adds a new document to a specified collection if it does not already exist.

    Args:
        collection_name (str): Name of the collection to update.
        document_data (object): Object containing the document content and metadata.
    
    Returns:
        str: Status message indicating the result of the operation.
    """
    # Initialize the specified collection
    collection = collection_init(collection_name)
    # Create a document object
    document = Document(ids=[message_id],page_content=message_text)
    # Check if the document already exists
    if document_exists(message_text, collection_name):
        return "exists"
    
    # Add the document to the collection
    collection.add_documents(documents=[document])
    return "added"

# def delete_document(documents_data, collection_name):
#     """
#     Deletes document from the specified collection using their IDs.

#     Args:
#         ids (list): List of document IDs to delete.
#         collection_name (str): Name of the collection to delete documents from.
#     """
#     # Initialize the specified collection
#     collection = collection_init(collection_name)
    
#     # Prepare and process each document
#     for document_data in documents_data.documents:
#           # Delete the documents by their IDs
#         collection.delete(ids=document_data.product_data.product_id)
    
#     return "The document has been deleted successfully."


def retriever_collection(collection_name):
    # Initialize the specified collection
    collection = collection_init(collection_name)
    
    retriever = collection.as_retriever(
      search_type="mmr",
      search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
      )
    
    return retriever

   

def document_exists(document: str, collection_name: str, threshold: float = 0.9) -> bool:
    """
    Check if a document already exists in the specified collection by comparing embeddings.

    Args:
        document (str): The document content to check.
        collection_name (str): The name of the collection.
        threshold (float): Similarity score threshold to determine if a document exists.

    Returns:
        bool: True if the document exists, False otherwise.
    """
     # Initialize the specified collection
    collection = collection_init(collection_name)

    # Perform similarity search with score in the collection
    results = collection.similarity_search_with_score(
        document,
        k=1,  # Retrieve the most similar document
    )

    # Process the results
    for res, score in results:
        if score <= threshold:
            return True  # Document exists

    return False  # Document does not exist