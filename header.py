import stremlit as st

def get_traditional_rags_desc():
   
    st.markdown("""
    #### What is RAG (Retrieval-Augmented Generation)
    It is an AI technique that combines document retrieval with generative models to answer questions using both external knowledge and language understanding.
    """)

    st.markdown("""
    ##### What is NOT RAG?
    RAG does not rely solely on the language model's internal knowledge or training data. It does not generate answers without consulting external sources or documents.

    **Example:**  
    A standard chatbot that answers questions only using its pre-trained model (without searching or retrieving any documents) is NOT a RAG system.  
    A RAG system, in contrast, retrieves relevant documents (e.g., PDFs, web pages) and uses them to generate more accurate and context-aware answers.

    **Is web search + LLM a RAG?**  
    If you perform a web search, retrieve relevant documents or snippets, and then use an LLM to answer based on those retrieved results, this is considered a RAG approach.  
    If you only use the LLM to answer without retrieving and using external content, it is NOT RAG.
    """)


def get_agentic_rags_desc():
    st.markdown("""
    #### What is Agentic RAG?
    Agentic RAG extends traditional RAG by introducing intelligent routing, dynamic source selection (local documents, web search, or hybrid), and advanced reasoning to optimize answer quality and transparency.
    """)

def get_steps():
    st.markdown("""
        ##### 📝 How to Use This App

        1. **Upload your documents:** Use the uploader below to add your PDF files. These will form your custom knowledge base.
        2. **Ask your question:** Enter any question in the input box or select a sample from the sidebar.
        3. **Intelligent routing:** The Agentic RAG system will automatically decide the best way to answer:
            - **Local:** Uses your uploaded documents for answers when relevant.
            - **Web:** Performs a web search if your question requires up-to-date or external information.
            - **Hybrid:** Combines both local documents and web sources for comprehensive responses.
        """)
    
