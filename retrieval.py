
def get_local_content(
        vector_db, 
        query: str, 
        k: int = 3
    ) -> dict:
    
    """Retrieve content from vector database with detailed information"""
    try:
        docs_with_scores = vector_db.similarity_search_with_score(query, k=k)
        
        content_pieces = []
        source_details = []
        
        for i, (doc, score) in enumerate(docs_with_scores):
            content_pieces.append(doc.page_content)
            source_details.append({
                "chunk_id": i + 1,
                "similarity_score": round(1 - score, 3),  # Convert distance to similarity
                "source_file": doc.metadata.get('source', 'Unknown'),
                "page": doc.metadata.get('page', 'N/A'),
                "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "content_length": len(doc.page_content)
            })
        
        return {
            "content": ' '.join(content_pieces),
            "source_details": source_details,
            "total_chunks": len(docs_with_scores),
            "avg_similarity": round(sum([1 - score for _, score in docs_with_scores]) / len(docs_with_scores), 3) if docs_with_scores else 0
        }
    except Exception as e:
        print(f"Error in get_local_content: {e}")
        return {
            "content": "",
            "source_details": [],
            "total_chunks": 0,
            "avg_similarity": 0
        }

def traditional_rag_simple_retrieval(
        vector_db, 
        query: str, 
        k: int = 2
    ) -> str:
    """Simplified retrieval for traditional RAG - more basic approach"""
    try:
        # Use fewer documents and simpler retrieval
        docs = vector_db.similarity_search(query, k=k)
        # Just concatenate without sophisticated processing
        content = " ".join([doc.page_content[:300] for doc in docs])  # Limit content
        return content
    except:
        return ""
