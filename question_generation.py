

def generate_dynamic_questions(doc_chunks, llm):
    
    """Generate relevant questions based on uploaded content"""
    
    if not doc_chunks:
        return []
    
    # Sample content from chunks
    sample_content = " ".join([chunk.page_content[:200] for chunk in doc_chunks[:3]])
    
    question_prompt = f"""Based on the following document content, generate 6 relevant questions that would test both local knowledge retrieval and require current/external information.

        Content: {sample_content}

        Generate questions in two categories:
        1. Three questions that can be answered from the document content (LOCAL)
        2. Three questions that would require external/current information (WEB)

        Format as:
        LOCAL: question1
        LOCAL: question2  
        LOCAL: question3
        WEB: question1
        WEB: question2
        WEB: question3

        Questions:"""
            
    try:
        response = llm.invoke(question_prompt)
        questions_text = response.content.strip()
        
        local_questions = []
        web_questions = []
        
        for line in questions_text.split('\n'):
            line = line.strip()
            if line.startswith('LOCAL:'):
                local_questions.append(line[6:].strip())
            elif line.startswith('WEB:'):
                web_questions.append(line[4:].strip())
        
        return local_questions, web_questions
        
    except:
        # Fallback questions
        return [
            "What is the main topic of the document?",
            "What are the key concepts mentioned?",
            "What are the main benefits discussed?"
        ], [
            "What are the latest developments in this field?",
            "What are current market trends related to this topic?",
            "What are recent news articles about this subject?"
        ]
