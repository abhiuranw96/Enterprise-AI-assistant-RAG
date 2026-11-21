from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import Iterable

def chunk_documents(documents: Iterable[Document]) -> list[Document]:
    """
    Chunk a list of Document objects into smaller chunks based on the specified chunk size and overlap.
    
    Args:
        documents (Iterable[Document]): An iterable of Document objects to be chunked.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,  # You can adjust this value based on your requirements
        chunk_overlap=150,  # You can adjust this value based on your requirements
        add_start_index=True,
    )
    
    return text_splitter.split_documents(list(documents))
    
   
    
    