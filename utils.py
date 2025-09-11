import os
import streamlit as st

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
    
    # Fallback to environment variables (for other deployments)
    groq_key = os.getenv("GROQ_API_KEY", "")
    serper_key = os.getenv("SERPER_API_KEY", "")
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    
    return groq_key, serper_key, gemini_key