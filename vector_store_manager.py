import os
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from config import EMBEDDING_MODEL, VECTOR_STORE_TABLE


class VectorStoreManager:
    """Manage vector store operations with FAISS."""
    
    def __init__(self, persist_directory: str = "faiss_index"):
        """
        Initialize FAISS vector store.
        
        Args:
            persist_directory: Directory to save/load FAISS index
        """
        self.persist_directory = persist_directory
        self.index_path = os.path.join(persist_directory, VECTOR_STORE_TABLE)
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        
        # Initialize or load vector store
        if os.path.exists(self.index_path) and os.path.isdir(self.index_path):
            # Load existing index
            self.vector_store = FAISS.load_local(
                self.index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"✅ Loaded existing FAISS index from {self.index_path}")
        else:
            # Create new empty index (will be populated when documents are added)
            self.vector_store = None
            print(f"📝 Will create new FAISS index at {self.index_path}")
    
    def add_documents(self, documents: List[Document]) -> int:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Number of documents added
        """
        if self.vector_store is None:
            # Create new FAISS index from documents
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            print(f"✅ Created new FAISS index with {len(documents)} documents")
        else:
            # Add documents to existing index
            self.vector_store.add_documents(documents)
            print(f"✅ Added {len(documents)} documents to existing index")
        
        # Save the index
        self.save()
        
        return len(documents)
    
    def get_retriever(self, search_kwargs: dict = None):
        """
        Get a retriever for the vector store.
        
        Args:
            search_kwargs: Optional search parameters
            
        Returns:
            Retriever object
        """
        if self.vector_store is None:
            raise ValueError("Vector store is empty. Add documents first.")
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        if self.vector_store is None:
            raise ValueError("Vector store is empty. Add documents first.")
        
        return self.vector_store.similarity_search(query, k=k)
    
    def save(self):
        """Save the FAISS index to disk."""
        if self.vector_store is not None:
            self.vector_store.save_local(self.index_path)
            print(f"💾 Saved FAISS index to {self.index_path}")
    
    def delete(self):
        """Delete the FAISS index from disk."""
        import shutil
        if os.path.exists(self.index_path):
            shutil.rmtree(self.index_path)
            print(f"🗑️  Deleted FAISS index at {self.index_path}")
            self.vector_store = None
    
    def get_stats(self) -> dict:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with stats
        """
        if self.vector_store is None:
            return {
                "total_documents": 0,
                "index_exists": False
            }
        
        # FAISS doesn't directly expose document count, so we estimate
        return {
            "total_documents": "Unknown (FAISS limitation)",
            "index_exists": True,
            "index_path": self.index_path
        }