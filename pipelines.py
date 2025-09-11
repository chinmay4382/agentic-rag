from visualization import create_sankey_diagram
from routing import check_local_knowledge_enhanced
from answer_generation import generate_answer_enhanced
from retrieval import get_local_content, get_web_content_enhanced, traditional_rag_simple_retrieval
from utils import get_api_keys
import time 

def traditional_rag_query_enhanced(llm, vector_db, query: str) -> dict:
    """Enhanced traditional RAG with simpler, more basic behavior"""
    start_time = time.time()
    
    # Traditional RAG: Simple, fixed approach
    context = traditional_rag_simple_retrieval(vector_db, query, k=2)  # Fewer docs
    answer = generate_answer_enhanced(llm, context, query, "local")
    
    processing_time = time.time() - start_time
    
    return {
        "answer": answer,
        "source_type": "local",
        "processing_time": processing_time,
        "context_length": len(context),
        "route_decision": "LOCAL (Fixed)",
        "routing_explanation": "Traditional RAG always uses local documents with basic retrieval",
        "processing_steps": [
            "Fixed local document search",
            "Basic similarity matching", 
            "Simple answer generation"
        ],
        "intelligence_level": "Basic"
    }

def agentic_rag_query_enhanced(llm, vector_db, query: str) -> dict:
    """Enhanced Agentic RAG with sophisticated routing and detailed transparency"""
    start_time = time.time()
    processing_steps = []
    
    # Step 1: Intelligent analysis
    processing_steps.append("Analyzing query intent and context")
    local_sample = get_local_content(vector_db, "sample", k=2)
    sample_context = local_sample["content"] if isinstance(local_sample, dict) else str(local_sample)
    
    # Step 2: Advanced routing decision with detailed analysis
    processing_steps.append("Making intelligent routing decision with confidence scoring")
    # Get actual relevant context for the query instead of just sample
    query_context = get_local_content(vector_db, query, k=3)
    actual_context = query_context["content"] if isinstance(query_context, dict) else str(query_context)
    routing_result = check_local_knowledge_enhanced(llm, query, actual_context)
    route = routing_result["route"]
    
    # Step 3: Source-specific retrieval with detailed tracking
    sources = []
    local_source_details = []
    web_metadata = {}
    context_parts = []
    
    if route == "LOCAL":
        processing_steps.append("Retrieving from curated knowledge base with similarity scoring")
        local_result = get_local_content(vector_db, query, k=4)
        context = local_result["content"]
        source_type = "local"
        local_source_details = local_result["source_details"]
        
    elif route == "WEB":
        processing_steps.append("Searching web for current information with source tracking")
        web_result = get_web_content_enhanced(query)
        context = web_result["content"]
        sources = web_result["sources"]
        web_metadata = web_result.get("search_metadata", {})
        source_type = "web"
        
    else:  # HYBRID routing
        processing_steps.append("Retrieving from local knowledge base")
        local_result = get_local_content(vector_db, query, k=3)
        local_context = local_result["content"]
        local_source_details = local_result["source_details"]
        context_parts.append(f"**Local Knowledge:**\n{local_context}")
        
        processing_steps.append("Searching web for additional current information")
        web_result = get_web_content_enhanced(query)
        web_context = web_result["content"]
        sources = web_result["sources"]
        web_metadata = web_result.get("search_metadata", {})
        context_parts.append(f"**Current Web Information:**\n{web_context}")
        
        # Combine both contexts
        context = "\n\n".join(context_parts)
        source_type = "hybrid"
    
    # Step 4: Enhanced answer generation with quality check
    processing_steps.append("Generating contextually-aware response with source attribution")
    answer = generate_answer_enhanced(llm, context, query, source_type, sources)
    
    # Step 5: Quality check for LOCAL routing - fallback to WEB if answer is poor
    if route == "LOCAL" and routing_result.get("confidence", "medium").lower() != "high":
        # Check if the answer seems incomplete or generic
        if len(answer) < 100 or "I don't have" in answer or "not available" in answer.lower() or "cannot find" in answer.lower():
            processing_steps.append("Local answer insufficient - falling back to web search")
            web_result = get_web_content_enhanced(query)
            web_context = web_result["content"]
            web_sources = web_result["sources"]
            web_metadata = web_result.get("search_metadata", {})
            
            # Generate new answer with web content
            fallback_answer = generate_answer_enhanced(llm, web_context, query, "web", web_sources)
            
            # Update results to reflect the fallback
            answer = fallback_answer
            context = web_context
            source_type = "web"
            sources = web_sources
            web_metadata = web_metadata
            route = "WEB (Fallback)"
            routing_result["reasoning"] += " [System detected insufficient local information and switched to web search]"
    
    processing_time = time.time() - start_time
    
    return {
        "answer": answer,
        "source_type": source_type,
        "processing_time": processing_time,
        "context_length": len(context),
        "route_decision": route,
        "routing_explanation": routing_result["reasoning"],
        "routing_confidence": routing_result["confidence"],
        "context_match_score": routing_result.get("context_match_score", 0),
        "temporal_requirement": routing_result.get("temporal_requirement", "NO"),
        "full_routing_analysis": routing_result.get("full_analysis", ""),
        "processing_steps": processing_steps,
        "intelligence_level": "Advanced",
        "sources": sources,
        "local_source_details": local_source_details,
        "web_metadata": web_metadata,
        "total_sources_used": len(local_source_details) if source_type == "local" else len(sources)
    }
