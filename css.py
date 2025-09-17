import streamlit as st

def apply_custom_css():
    """Apply enhanced custom CSS styles to the Streamlit app"""

    st.set_page_config(
        page_title="Agentic RAG vs Traditional RAG , Try yourself",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Enhanced custom CSS
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2e8b57;
            margin: 1rem 0;
        }
        .pipeline-box {
            border: 2px solid #e1e5e9;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .traditional-rag {
            border-left: 5px solid #ff6b6b;
            background: linear-gradient(135deg, #ffe0e0 0%, #ffcccc 100%);
        }
        .agentic-rag {
            border-left: 5px solid #4ecdc4;
            background: linear-gradient(135deg, #e0f7f7 0%, #ccf2f2 100%);
        }
        .routing-decision {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.8rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .local-route {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border: 2px solid #28a745;
        }
        .web-route {
            background: linear-gradient(135deg, #cce5ff 0%, #99d6ff 100%);
            color: #004085;
            border: 2px solid #007bff;
        }
        .fixed-route {
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
            color: #721c24;
            border: 2px solid #dc3545;
        }
        .hybrid-route {
            background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
            color: #00695c;
            border: 2px solid #00acc1;
        }
        .upload-area {
            border: 2px dashed #007bff;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            background: #f8f9ff;
            margin: 1rem 0;
        }
        .pipeline-step {
            display: inline-block;
            padding: 0.5rem 1rem;
            margin: 0.2rem;
            border-radius: 20px;
            background: #e9ecef;
            border: 1px solid #ced4da;
            font-size: 0.9rem;
        }
        .step-active {
            background: #28a745;
            color: white;
            border: 1px solid #28a745;
        }
        .step-traditional {
            background: #ff6b6b;
            color: white;
            border: 1px solid #ff6b6b;
        }
        .step-agentic {
            background: #4ecdc4;
            color: white;
            border: 1px solid #4ecdc4;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
