import streamlit as st
from utils import get_api_keys, initialize_base_components,FAISS
from css import apply_custom_css
from knowledge_base import process_uploaded_pdf
from question_generation import generate_dynamic_questions
import time
from pipelines import traditional_rag_query_enhanced, agentic_rag_query_enhanced
from visualization import create_processing_steps_visual, create_pipeline_visualization
from header import *


if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.query_history = []
    st.session_state.components_loaded = False
    st.session_state.custom_docs_loaded = False
    st.session_state.dynamic_questions = []
    st.session_state.current_knowledge_base = "default"



def main():
    """Enhanced main Streamlit application"""
    apply_custom_css()
    # Header
    st.markdown('<div class="main-header">🤖 Agentic RAG : AI and SEARCH</div>', unsafe_allow_html=True)
    get_traditional_rags_desc()
    get_agentic_rags_desc()
    get_steps()

    if not st.session_state.components_loaded:
        llm, embeddings = initialize_base_components()
        if llm and embeddings:
            st.session_state.llm = llm
            st.session_state.embeddings = embeddings
            st.session_state.components_loaded = True

    
    # Sidebar
    with st.sidebar:
        with st.expander("### 🔑 API Configuration"):
            # API Keys Status Section            
            # Check API key availability from environment
            groq_key, serper_key, gemini_key = get_api_keys()
            
            if groq_key and serper_key:
                st.success("✅ API keys configured from environment")
                st.markdown("**🟢 Status:** Ready to use all features")
            else:
                st.error("❌ API keys not found in environment variables")
                st.markdown("**🔴 Status:** Please configure environment variables")
                st.info("💡 Required: GROQ_API_KEY, SERPER_API_KEY, GEMINI_API_KEY")
        
        with st.expander("### 📄 Upload Documents"):
            uploaded_files = st.file_uploader(
                "Upload PDF files to create custom knowledge base",
                type=['pdf'],
                accept_multiple_files=True,
                help="Upload PDF documents to train the RAG system on your content"
            )

            if uploaded_files and st.button("🚀 Process & Train", type="primary"):
                with st.spinner("Processing uploaded documents..."):
                    # Initialize base components if not already done
                    if not st.session_state.components_loaded:
                        llm, embeddings = initialize_base_components()
                        if llm and embeddings:
                            st.session_state.llm = llm
                            st.session_state.embeddings = embeddings
                            st.session_state.components_loaded = True
                
                # Process uploaded PDFs
                all_chunks = []
                for uploaded_file in uploaded_files:
                    st.write(f"Processing: {uploaded_file.name}")
                    vector_db, chunks = process_uploaded_pdf(uploaded_file, st.session_state.embeddings)
                    if chunks:
                        all_chunks.extend(chunks)
                
                if all_chunks:
                    # Create combined vector database
                    st.session_state.vector_db = FAISS.from_documents(all_chunks, st.session_state.embeddings)
                    st.session_state.custom_docs_loaded = True
                    st.session_state.current_knowledge_base = "custom"
                    
                    # Generate dynamic questions
                    local_q, web_q = generate_dynamic_questions(all_chunks, st.session_state.llm)
                    st.session_state.dynamic_questions = {
                        'local': local_q,
                        'web': web_q
                    }
                    
                    st.success(f"✅ Processed {len(uploaded_files)} files ({len(all_chunks)} chunks)")
                    
                else:
                    st.error("❌ No valid text chunks extracted from uploaded PDFs.")   
                time.sleep(3)
                st.rerun()

        with st.expander("🔧 System Architecture"):
            st.markdown("""
            **Traditional RAG:**
            - ❌ Fixed local-only retrieval
            - ❌ Basic similarity search
            - ❌ Simple answer generation
            - ❌ No intelligence or adaptation
            
            **Agentic RAG:**
            - ✅ Intelligent routing system
            - ✅ Advanced retrieval strategies
            - ✅ Multi-source information fusion
            - ✅ Context-aware processing
            - ✅ Quality assessment & optimization
            """)

    st.markdown('<div class="sub-header">💬 Ask Your Question</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "Enter your question:",
            value=st.session_state.get('selected_query', ''),
            placeholder="Ask anything - the system will intelligently route to the best source...",
            key="query_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        process_query = st.button("🚀 Process Query", type="primary")

    if process_query and query:
        st.markdown("---")
        
        # Process both systems
        with st.spinner("Processing with both RAG systems..."):
            traditional_result = traditional_rag_query_enhanced(
                st.session_state.llm, 
                st.session_state.vector_db, 
                query
            )
            
            agentic_result = agentic_rag_query_enhanced(
                st.session_state.llm,
                st.session_state.vector_db,
                query
            )
        
        # Display results in two columns
        
        
        # Agentic RAG Results
        st.markdown('<div class="pipeline-box agentic-rag">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">🤖 Agentic RAG</div>', unsafe_allow_html=True)
        
        # Route indicator
        if agentic_result["route_decision"] == "LOCAL":
            route_class = "local-route"
        elif agentic_result["route_decision"] == "WEB":
            route_class = "web-route"
        else:  # HYBRID
            route_class = "hybrid-route"
        st.markdown(f'<div class="routing-decision {route_class}">{agentic_result["route_decision"]} Route</div>', unsafe_allow_html=True)
        st.success(agentic_result["routing_explanation"])
        
        # Processing steps
        st.markdown("**Processing Pipeline:**")
        steps_html = create_processing_steps_visual(agentic_result["processing_steps"], "agentic")
        st.markdown(steps_html, unsafe_allow_html=True)
        
        # Answer
        st.markdown("**Answer:**")
        st.write(agentic_result["answer"])
        
        # ===== ENHANCED TRANSPARENCY SECTION =====
        st.markdown("---")
        st.markdown("**🔍 Transparency & Source Attribution**")
        
        # Routing Decision Details
        with st.expander("🧭 Detailed Routing Analysis", expanded=True):
            st.markdown(f"**Route Decision:** {agentic_result['route_decision']}")
            st.markdown(f"**Confidence Level:** {agentic_result.get('routing_confidence', 'Unknown').title()}")
            st.markdown(f"**Context Match Score:** {agentic_result.get('context_match_score', 0):.3f}")
            st.markdown(f"**Temporal Requirement:** {agentic_result.get('temporal_requirement', 'Unknown')}")
            st.markdown(f"**Reasoning:** {agentic_result['routing_explanation']}")
            
            # Full routing analysis
            with st.expander("📋 Complete Router Analysis"):
                st.text(agentic_result.get('full_routing_analysis', 'Analysis not available'))
        
        # Source Details
        if agentic_result['route_decision'] in ['LOCAL', 'HYBRID']:
            # Local source details
            with st.expander("📚 Local Document Sources", expanded=True):
                local_details = agentic_result.get('local_source_details', [])
                if local_details:
                    st.markdown(f"**Total Chunks Used:** {len(local_details)}")
                    
                    for detail in local_details:
                        st.markdown(f"**Chunk {detail['chunk_id']}:**")
                        col_a, col_b, col_c = st.columns([2, 1, 1])
                        
                        with col_a:
                            st.markdown(f"**Source:** {detail['source_file']}")
                            st.markdown(f"**Page:** {detail.get('page', 'N/A')}")
                        with col_b:
                            st.metric("Similarity", f"{detail['similarity_score']:.3f}")
                        with col_c:
                            st.metric("Length", f"{detail['content_length']} chars")
                        
                        with st.expander(f"Preview Chunk {detail['chunk_id']}"):
                            st.text(detail['content_preview'])
                        
                        st.markdown("---")
                else:
                    st.info("No detailed source information available")
        
        
        if agentic_result['route_decision'] in ['WEB', 'HYBRID']:
            # Web source details
            with st.expander("🌐 Web Search Sources", expanded=True):
                web_sources = agentic_result.get('sources', [])
                web_metadata = agentic_result.get('web_metadata', {})
                
                # Search metadata
                st.markdown("**Search Information:**")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Search Time", f"{web_metadata.get('search_time', 0):.3f}s")
                with col_b:
                    st.metric("Results Found", web_metadata.get('total_results', 'Unknown'))
                with col_c:
                    st.metric("Sources Used", len(web_sources))
                
                st.markdown(f"**Search Query:** {web_metadata.get('search_query', query)}")
                
                # Individual sources
                st.markdown("**Source Details:**")
                for i, source in enumerate(web_sources, 1):
                    st.markdown(f"**Source {i}: {source.get('title', 'Unknown')}**")
                    col_a, col_b = st.columns([3, 1])
                    
                    with col_a:
                        st.markdown(f"**Domain:** {source.get('domain', 'Unknown')}")
                        if source.get('link'):
                            st.markdown(f"**URL:** [Link]({source['link']})")
                    with col_b:
                        st.metric("Position", source.get('position', i))
                        st.metric("Snippet Length", f"{source.get('snippet_length', 0)} chars")
                    
                    with st.expander(f"Preview Source {i}"):
                        st.text(source.get('snippet', 'No preview available'))
                    
                    st.markdown("---")
        
        # Metrics
        col2a, col2b, col2c = st.columns(3)
        with col2a:
            st.metric("Time", f"{agentic_result['processing_time']:.2f}s")
        with col2b:
            st.metric("Context", f"{agentic_result['context_length']} chars")
        with col2c:
            st.metric("Intelligence", agentic_result["intelligence_level"])
        
        # Pipeline visualization
        # agentic_fig = create_pipeline_visualization("agentic", agentic_result["route_decision"], agentic_result["processing_steps"])
        # st.plotly_chart(agentic_fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        

if __name__ == "__main__":
    main()
