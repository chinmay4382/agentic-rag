import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI




def initialize_base_components():
    """Initialize base RAG components"""
    try:
        
        # Get API keys from session state or environment
        groq_key, serper_key, gemini_key = get_api_keys()
       
        if not groq_key:
            st.error("❌ Groq API key required for LLM functionality")
            return None, None
        
        # Initialize LLM
        llm = ChatGroq(
            model='llama-3.1-8b-instant',
            temperature=0,
            max_tokens=1000,
            timeout=None,
            max_retries=2,
            api_key=groq_key
        )
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-mpnet-base-v2',
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        return llm, embeddings
        
    except Exception as e:
        st.error(f"Error initializing base components: {e}")
        return None, None       
    
    # llm = ChatGoogleGenerativeAI(
        #     model="gemini-2.5-flash",   # explicitly call Gemini 2.5 Pro
        #     temperature=0,
        #     max_output_tokens=500,    # Gemini uses max_output_tokens instead of max_tokens
        #     timeout=None,
        #     max_retries=2,
        #     google_api_key=gemini_key
        # )
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-mpnet-base-v2',
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        return llm, embeddings
        
    except Exception as e:
        st.error(f"Error initializing base components: {e}")
        return None, None

def get_api_keys():
    """Get API keys from Streamlit secrets or environment variables"""
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        
        groq_key = st.secrets.get("GROQ_API_KEY", "")
        serper_key = st.secrets.get("SERPER_API_KEY", "")
        gemini_key = st.secrets.get("GEMINI_API_KEY", "")
        
        # If found in secrets, return them
        if gemini_key and serper_key:
            return groq_key, serper_key, gemini_key
    except:
        pass
    # Load from .env file if exists (for local development)
    load_dotenv()
    # Fallback to environment variables (for other deployments)
    groq_key = os.getenv("GROQ_API_KEY", "")
    serper_key = os.getenv("SERPER_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    st.balloons
    return groq_key, serper_key, gemini_key