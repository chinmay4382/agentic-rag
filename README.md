# AGENTIC-RAG
The Agentic RAG dynamically routes user queries to the most relevant sources—local documents, web search, or both—based on the query context by providing transparency into the decision-making process to help users.

## 🔍 Features
- Context-aware query routing
- Integration with local document stores and web search
- Transparent decision-making logic
- Modular and extensible architecture

## ⚙️ How It Works
1. **Query Analysis**: Determines the nature of the user query.
2. **Source Selection**: Routes the query to:
   - Local documents
   - Web search
   - Or both, depending on context
3. **Response Generation**: Uses retrieved information to generate a coherent answer.
4. **Transparency Layer**: Explains why a particular source was chosen.

## 🛠️  Tools Used
1. **LangChain**: Framework for building context-aware agents and chaining LLM calls with external tools..
2. **Streamlit**: Interactive frontend for user input and real-time response visualization.
3. **FAISS**: Efficient similarity search for retrieving relevant local documents..
4. **Groq’s Llama 3.1-8B**: High-performance language model for generating accurate and context-rich responses by META.
5. **Serper**: Fast and reliable web search API for retrieving up-to-date information from the internet.
6. **Hugging Face**: Access to pre-trained models and tokenizers for NLP tasks and experimentation.


## 🧭  Architecture
<img src="AR%20architecture.png" width="420px" height="420px" align="left">
<br><br><br><br><br><br><br><br><br><br><br><br><br><br>

## 🚀 Installation

```bash
git clone https://github.com/chinmay4382/agentic-rag.git
cd agentic-rag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## 🧪 Usage

```bash
streamlit run main.py
```
