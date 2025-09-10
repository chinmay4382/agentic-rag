from langchain.schema import Document

default_docs = [
        
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
        ),
        Document(
            page_content="""Artificial Intelligence and Machine Learning: Core Concepts
            
            Machine learning forms the backbone of modern AI applications, enabling systems
            to learn and improve from experience without explicit programming.
            
            The three fundamental paradigms of machine learning are:
            
            **1. Supervised Learning**
            - Learns from labeled training examples
            - Goal: Predict outputs for new inputs
            - Examples: Classification, regression, object detection
            - Algorithms: Neural networks, decision trees, SVM, random forests
            - Applications: Email filtering, medical diagnosis, financial forecasting
            
            **2. Unsupervised Learning**
            - Discovers patterns in unlabeled data
            - Goal: Find hidden structures and relationships
            - Examples: Clustering, dimensionality reduction, anomaly detection
            - Algorithms: K-means, PCA, autoencoders, GANs
            - Applications: Customer segmentation, data compression, fraud detection
            
            **3. Reinforcement Learning**
            - Learns through interaction with environment
            - Goal: Maximize cumulative rewards through optimal actions
            - Examples: Game playing, robotics, resource allocation
            - Algorithms: Q-learning, policy gradients, actor-critic methods
            - Applications: Autonomous vehicles, trading systems, recommendation engines
            
            Modern applications leverage deep learning, transfer learning, and ensemble methods
            to achieve state-of-the-art performance across diverse domains.""",
            metadata={'source': 'ai_ml_handbook.pdf', 'page': 1, 'type': 'educational'}
        )
        
    ]