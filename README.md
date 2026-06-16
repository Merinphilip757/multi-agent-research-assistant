# 🤖 DeepAgents — Multi-Agent Research Assistant

> A LangGraph-powered multi-agent pipeline that generates in-depth research reports from a single query — featuring a Planner, Researcher, Critic, and Final Writer working in sequence, served via a Streamlit UI.

---

## 📌 Overview

**DeepAgents** is a multi-agent AI research assistant built with **LangGraph** and **Groq's Llama models**. You enter a research topic, and a team of four specialized AI agents collaborates through a structured graph to produce a comprehensive, reviewed research report — which you can download as `.txt` or `.md`.

---

## 🧠 Agent Architecture

The system implements a **linear LangGraph state machine** with four sequential nodes:

```
[User Query]
     │
     ▼
┌─────────────┐
│   Planner   │  → Creates a structured research plan
└──────┬──────┘
       │
       ▼
┌──────────────┐
│  Researcher  │  → Conducts research based on the plan
└──────┬───────┘
       │
       ▼
┌────────────┐
│   Critic   │  → Reviews gaps, weak arguments, and improvements
└──────┬─────┘
       │
       ▼
┌──────────────────┐
│  Final Writer    │  → Synthesizes research + critique into final report
└──────────────────┘
```

| Agent | Role |
|---|---|
| **Planner** | Breaks down the query into a structured research plan |
| **Researcher** | Investigates the topic guided by the plan |
| **Critic** | Identifies missing info, weak arguments, and improvements |
| **Final Writer** | Produces the polished final report from research + critique |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Agentic Framework** | [LangGraph](https://github.com/langchain-ai/langgraph) |
| **LLM** | Groq — `llama-3.1-8b-instant` / `llama-3.3-70b-versatile` |
| **LLM Integration** | `langchain-groq` |
| **Frontend** | [Streamlit](https://streamlit.io) |
| **State Management** | `TypedDict` shared state across all agents |
| **Config** | `python-dotenv` |

---

## 📁 Project Structure

```
multi-agent-research-assistant/
│
├── streamlit_app.py      # Main app: LangGraph graph + Streamlit UI
└── requirement.txt       # Python dependencies
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Merinphilip757/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirement.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## 🚀 Usage

1. Open the Streamlit app in your browser.
2. (Optional) Adjust the model and temperature in the **sidebar**.
3. Enter your research topic in the text area.
4. Click **🚀 Generate Report**.
5. View the **Final Report** tab for the synthesized output.
6. Switch to **Agent Logs** to inspect each agent's intermediate output.
7. Download the report as `.txt` or `.md`.

---

## 🔧 Configuration (Sidebar)

| Setting | Options | Default |
|---|---|---|
| **Model** | `llama-3.3-70b-versatile`, `llama-3.1-8b-instant` | `llama-3.1-8b-instant` |
| **Temperature** | 0.0 – 1.0 | 0.2 |

---

## 📦 Dependencies

```
streamlit
langgraph
langchain
langchain-core
langchain-groq
python-dotenv
typing-extensions
```

---

## 🗂️ Shared Agent State

All agents communicate through a single `TypedDict` state object passed through the LangGraph graph:

```python
class AgentState(TypedDict):
    query: str          # Original user query
    plan: str           # Planner's research plan
    research: str       # Researcher's findings
    review: str         # Critic's feedback
    final_answer: str   # Final synthesized report
```

---

## 💡 How LangGraph Is Used

- `StateGraph` defines the agent graph with `AgentState` as shared memory.
- Each agent is a **node** that reads from and writes to the shared state.
- `add_edge` creates a deterministic linear flow: `planner → researcher → critic → final_writer → END`.
- The compiled graph is invoked with the user query to trigger the full pipeline.

---

## 📄 License

This project is open source. Feel free to fork, extend, or build upon it.

---

## 🙌 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- [Groq](https://groq.com) for ultra-fast LLM inference
- [Streamlit](https://streamlit.io) for rapid UI development
