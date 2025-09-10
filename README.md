# agentic-rag
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

## 🚀 Installation

```bash
git clone https://github.com/chinmay4382/agentic-rag.git
cd agentic-rag
python3 -n venv venv
source venv/bin/activate
pip install -r requirements.txt

## 🧪 Usage

```bash
streamlit run main.py

