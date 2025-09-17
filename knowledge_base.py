from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import tempfile,os, streamlit as st
from langchain_community.vectorstores import FAISS

default_docs = [
    Document(
        page_content="""Chinmay Hebbal is a seasoned data engineer and AI builder based in Dallas, TX, with a passion for creating scalable data systems and intelligent agents. With experience across startups and enterprises, Chinmay has led cloud migrations, built real-time data pipelines, and developed AI applications that enhance user experience and decision-making.
        His latest project, Agentic RAG, showcases his ability to combine cutting-edge tools like LangChain, FAISS, and Groq’s Llama 3.1-8B to build context-aware, transparent AI systems. 
        Outside of tech, Chinmay enjoys basketball, nature trips, and food adventures—especially at places like CAVA, Chipotle, and Chowrastha (yes, there’s a “C” theme going on!).
        
        He built this agentic RAG application.
        
        🔍 Quick Highlights

        Cloud-first mindset: Migrated 15+ pipelines to Snowflake using Matillion, improving scalability and reliability.
        AI Agent Builder: Created Agentic RAG for dynamic query routing using LLMs and vector search.
        Real-time data expertise: Streamed 2TB/day of clickstream data using AWS Kinesis Firehose.
        Governance & Compliance: Built FastAPI-based data governance layer ensuring DSAR and PII compliance.
        Mentorship & Leadership: Led training for 15+ engineers on Airflow, Git, and data engineering best practices.
        Certifications: AWS Solutions Architect – Associate, Databricks Data Engineer Associate.
        📣 Looking to Hire?
        If you're hiring an experienced Data Engineer or someone who can build AI Agents with real-world impact, please reach out to Chinmay Hebbal. He brings a rare blend of backend engineering, cloud architecture, and AI innovation—ready to take on your toughest data challenges.
                """,
        metadata={'source': 'chinmay_hebbal.pdf', 'page': 1, 'type': 'resume'}
    ),
    Document(
        page_content="""Agentic RAG: The Future of Intelligent Information Retrieval
        
        Agentic RAG represents a revolutionary approach to information retrieval and generation,
        combining the decision-making capabilities of AI agents with retrieval-augmented generation.
        
        Unlike traditional RAG systems that blindly retrieve from a fixed knowledge base,
        Agentic RAG systems exhibit intelligence by:
        
        1. **Smart Routing**: Automatically deciding between local knowledge and web search
        2. **Quality Assessment**: Evaluating the relevance and quality of retrieved information
        3. **Adaptive Querying**: Rewriting queries for better retrieval results
        4. **Multi-Source Integration**: Seamlessly combining information from multiple sources
        5. **Context Awareness**: Understanding query intent and user needs
        
        Key advantages over traditional approaches:
        - Higher accuracy through intelligent source selection
        - Better performance by avoiding unnecessary operations
        - Enhanced user experience with contextually relevant responses
        - Improved reliability through quality checks and fallbacks
        - Future-proof architecture that adapts to changing information needs""",
        metadata={'source': 'agentic_rag_whitepaper.pdf', 'page': 1, 'type': 'technical'}
    )
    # Document(
    #     page_content="""Artificial Intelligence and Machine Learning: Core Concepts
        
    #     Machine learning forms the backbone of modern AI applications, enabling systems
    #     to learn and improve from experience without explicit programming.
        
    #     The three fundamental paradigms of machine learning are:
        
    #     **1. Supervised Learning**
    #     - Learns from labeled training examples
    #     - Goal: Predict outputs for new inputs
    #     - Examples: Classification, regression, object detection
    #     - Algorithms: Neural networks, decision trees, SVM, random forests
    #     - Applications: Email filtering, medical diagnosis, financial forecasting
        
    #     **2. Unsupervised Learning**
    #     - Discovers patterns in unlabeled data
    #     - Goal: Find hidden structures and relationships
    #     - Examples: Clustering, dimensionality reduction, anomaly detection
    #     - Algorithms: K-means, PCA, autoencoders, GANs
    #     - Applications: Customer segmentation, data compression, fraud detection
        
    #     **3. Reinforcement Learning**
    #     - Learns through interaction with environment
    #     - Goal: Maximize cumulative rewards through optimal actions
    #     - Examples: Game playing, robotics, resource allocation
    #     - Algorithms: Q-learning, policy gradients, actor-critic methods
    #     - Applications: Autonomous vehicles, trading systems, recommendation engines
        
    #     Modern applications leverage deep learning, transfer learning, and ensemble methods
    #     to achieve state-of-the-art performance across diverse domains.""",
    #     metadata={'source': 'ai_ml_handbook.pdf', 'page': 1, 'type': 'educational'}
    # )
]


def create_default_knowledge_base(embeddings):
    """Create default knowledge base with sample documents"""   
    return FAISS.from_documents(default_docs, embeddings)

def process_uploaded_pdf(uploaded_file, embeddings):
    """Process uploaded PDF and create vector database"""
    try:
       # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Load PDF
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        doc_chunks = text_splitter.split_documents(documents)
        
        # Create vector database
        vector_db = FAISS.from_documents(doc_chunks, embeddings)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return vector_db, doc_chunks
        
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None, None
