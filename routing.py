import time
import requests
import json
from typing import Optional
from utils import get_api_keys

def check_local_knowledge_enhanced(llm, query: str, context: str) -> dict:
    """Enhanced router with detailed reasoning and confidence scoring"""
    
    router_prompt = f"""You are an advanced query router for an Agentic RAG system. You must be VERY CAREFUL and PRECISE about routing decisions.

    Query: "{query}"
    Available Local Context: {context[:800]}...

    CRITICAL ANALYSIS REQUIREMENTS:
    1. EXACT Content Match: Does the local context contain the EXACT information needed to answer this specific query? Not just related topics, but the precise answer.
    2. Completeness Check: Can you provide a COMPLETE answer using ONLY the local context?
    3. Information Specificity: Is the query asking for specific details, personal information, or data that must be explicitly present?
    4. Temporal Requirements: Does the query need current/real-time information?

    STRICT Routing Decision Rules:
    - LOCAL: ONLY if the context contains the EXACT answer to the query
    - WEB: Current events, real-time data, personal information not in context, specific details absent from context
    - HYBRID: Query needs both foundational knowledge (in context) AND current/additional information

    Be CONSERVATIVE: If you're not 100% certain the local context can fully answer the query, route to WEB or HYBRID.

    Provide your analysis in this format:
    Route: LOCAL, WEB, or HYBRID
    Confidence: HIGH/MEDIUM/LOW
    Reasoning: [Explain WHY you chose this route - be specific about what information is/isn't available]
    Context_Match: [0.0-1.0 score for how well context matches the SPECIFIC query]
    Temporal_Need: [YES/NO - does query need current information]

    Decision:"""
    
    try:
        response = llm.invoke(router_prompt)
        decision_text = response.content.strip()
        
        # Parse the structured response
        lines = decision_text.split('\n')
        route = "LOCAL"
        confidence = "MEDIUM"
        reasoning = decision_text
        context_match = 0.5
        temporal_need = "NO"
        
        for line in lines:
            line = line.strip()
            if line.startswith("Route:"):
                if "HYBRID" in line.upper():
                    route = "HYBRID"
                elif "WEB" in line.upper():
                    route = "WEB"
                else:
                    route = "LOCAL"
            elif line.startswith("Confidence:"):
                confidence = line.split(":")[1].strip()
            elif line.startswith("Reasoning:"):
                reasoning = line.split(":", 1)[1].strip()
            elif line.startswith("Context_Match:"):
                try:
                    context_match = float(line.split(":")[1].strip())
                except:
                    context_match = 0.5
            elif line.startswith("Temporal_Need:"):
                temporal_need = line.split(":")[1].strip()
        
        return {
            "route": route,
            "reasoning": reasoning,
            "confidence": confidence.lower(),
            "context_match_score": context_match,
            "temporal_requirement": temporal_need,
            "full_analysis": decision_text
        }
    except Exception as e:
        return {
            "route": "LOCAL",
            "reasoning": f"Router error: {str(e)} - defaulting to local",
            "confidence": "low",
            "context_match_score": 0.0,
            "temporal_requirement": "UNKNOWN",
            "full_analysis": "Error in routing analysis"
        }
    

def get_web_content_enhanced(query: str) -> dict:
    """Enhanced web content retrieval with detailed source information"""
    # Get API keys from session state
    groq_key, serper_key, gemini_key = get_api_keys()
    
    if not serper_key:
        return {
            "content": "Web search unavailable - Serper API key not configured",
            "sources": [],
            "search_metadata": {
                "search_query": query,
                "error": "No API key configured",
                "status": "Failed"
            },
            "success": False,
            "result_count": 0
        }
    
    url = 'https://google.serper.dev/search'
    payload = {'q': query, 'num': 5}
    headers = {
        'X-API-KEY': serper_key,
        'Content-Type': 'application/json'
    }
    
    search_start_time = time.time()
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        search_time = time.time() - search_start_time
        
        if response.status_code == 200:
            results = response.json()
            
            # Extract search metadata
            search_metadata = {
                "search_query": query,
                "search_time": round(search_time, 3),
                "total_results": results.get('searchInformation', {}).get('totalResults', 'Unknown'),
                "search_time_google": results.get('searchInformation', {}).get('searchTime', 'Unknown')
            }
            
            if 'organic' in results:
                content_pieces = []
                sources = []
                
                for i, result in enumerate(results['organic'][:4]):
                    title = result.get('title', 'Untitled')
                    snippet = result.get('snippet', 'No description available')
                    link = result.get('link', '')
                    position = result.get('position', i+1)
                    
                    content_pieces.append(f"**Source {i+1}**: {title}\n{snippet}")
                    sources.append({
                        "position": position,
                        "title": title, 
                        "link": link,
                        "snippet": snippet,
                        "domain": link.split('/')[2] if '//' in link else 'Unknown domain',
                        "snippet_length": len(snippet)
                    })
                
                return {
                    "content": '\n\n'.join(content_pieces),
                    "sources": sources,
                    "search_metadata": search_metadata,
                    "success": True,
                    "result_count": len(sources),
                    "search_query_used": query
                }
        
        return {
            "content": f"Limited web search results for: {query}",
            "sources": [],
            "search_metadata": {
                "search_query": query,
                "search_time": round(search_time, 3),
                "error": f"HTTP {response.status_code}"
            },
            "success": False,
            "result_count": 0,
            "search_query_used": query
        }
        
    except Exception as e:
        return {
            "content": f"Web search error for query: {query}",
            "sources": [],
            "search_metadata": {
                "search_query": query,
                "search_time": round(time.time() - search_start_time, 3),
                "error": str(e)
            },
            "success": False,
            "result_count": 0,
            "search_query_used": query
        }