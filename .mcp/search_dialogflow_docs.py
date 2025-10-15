# search_dialogflow_docs.py
import chromadb
from sentence_transformers import SentenceTransformer
import json
from typing import List, Dict, Any
import os

class DialogflowDocSearch:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Use absolute path relative to this script's location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "dialogflow_chroma_db")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection(name="dialogflow_cx_docs")
        self.embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    def search(self, 
               query: str, 
               n_results: int = 5,
               filter_section: str = None,
               filter_content_type: str = None) -> Dict[str, Any]:
        """
        Advanced search with filtering capabilities
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Build filter if specified
        where_filter = {}
        if filter_section:
            where_filter['section'] = filter_section
        if filter_content_type:
            where_filter['content_type'] = filter_content_type
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter if where_filter else None,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = {
            'query': query,
            'results': []
        }
        
        if results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results['results'].append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i],
                    'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                })
        
        return formatted_results
    
    def keyword_search(self, keywords: List[str], n_results: int = 5) -> List[Dict]:
        """Search by keywords in metadata"""
        results = []
        
        for keyword in keywords:
            # Query with metadata filter
            query_results = self.collection.get(
                where={"keywords": {"$contains": keyword}},
                limit=n_results
            )
            
            if query_results['documents']:
                for i, doc in enumerate(query_results['documents']):
                    results.append({
                        'content': doc,
                        'metadata': query_results['metadatas'][i],
                        'matched_keyword': keyword
                    })
        
        return results
    
    def get_section_content(self, section_name: str) -> List[Dict]:
        """Retrieve all chunks from a specific section"""
        results = self.collection.get(
            where={"section": section_name},
            include=['documents', 'metadatas']
        )
        
        chunks = []
        if results['documents']:
            for i, doc in enumerate(results['documents']):
                chunks.append({
                    'content': doc,
                    'metadata': results['metadatas'][i]
                })
        
        # Sort by chunk_index
        chunks.sort(key=lambda x: x['metadata'].get('chunk_index', 0))
        return chunks


def search_documentation(query: str, n_results: int = 5) -> str:
    """
    Main search function for Claude Code integration
    """
    searcher = DialogflowDocSearch()
    results = searcher.search(query, n_results)
    
    if not results['results']:
        return "No relevant information found in the documentation."
    
    # Format for Claude
    context_parts = []
    for i, result in enumerate(results['results'], 1):
        context_parts.append(f"--- Result {i} ---")
        context_parts.append(f"Section: {result['metadata']['section']}")
        context_parts.append(f"Relevance: {result['relevance_score']:.2%}")
        context_parts.append(f"\n{result['content']}\n")
    
    return "\n".join(context_parts)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python search_dialogflow_docs.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    results = search_documentation(query)
    print(results)
