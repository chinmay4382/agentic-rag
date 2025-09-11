def generate_answer_enhanced(
        llm, 
        context: str, 
        query: str, 
        source_type: str, 
        sources: list = None
) -> str:
    """Enhanced answer generation with source attribution"""
    if source_type == "hybrid":
        answer_prompt = f"""You are an expert AI assistant. Use the provided context from both local knowledge and current web information to answer the user's question comprehensively.

    Context (includes both local knowledge and current web information): {context}

    Question: {query}

    Instructions:
    - Synthesize information from both local knowledge and web sources
    - Provide a comprehensive answer that leverages both types of information
    - Clearly distinguish between established knowledge and current information when relevant
    - Use clear formatting with bullet points or numbered lists when appropriate
    - Be specific and informative
    - Maintain a professional and helpful tone

    Answer:"""
    else:
        answer_prompt = f"""You are an expert AI assistant. Use the provided context to answer the user's question comprehensively and accurately.

    Context: {context}

    Question: {query}

    Instructions:
    - Provide a detailed, well-structured answer based on the context
    - Use clear formatting with bullet points or numbered lists when appropriate
    - Be specific and informative
    - If the context is limited, acknowledge this appropriately
    - Maintain a professional and helpful tone

    Answer:"""
    
    try:
        response = llm.invoke(answer_prompt)
        answer = response.content.strip()
        
        # Add source information
        if source_type in ["web", "hybrid"] and sources:
            source_info = "\n\n**Web Sources:**\n"
            for i, source in enumerate(sources[:3], 1):
                source_info += f"{i}. {source.get('title', 'Unknown source')}\n"
            answer += source_info
        
        return answer
    except Exception as e:
        return f"Error generating answer: {str(e)}"
