import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# Shared State
class AgentState(TypedDict):
    query: str
    plan: str
    research: str
    review: str
    final_answer: str

# Planner Node
def planner(state):

    prompt = f"""
    Create a research plan for:

    {state['query']}
    """

    plan = llm.invoke(prompt).content

    return {
        "plan": plan
    }

# Research Node
def researcher(state):

    prompt = f"""
    Research this topic:

    {state['query']}

    Plan:
    {state['plan']}
    """

    research = llm.invoke(prompt).content

    return {
        "research": research
    }

# Critic Node
def critic(state):

    prompt = f"""
    Review the following research.

    Research:
    {state['research']}

    Identify:
    - Missing information
    - Weak arguments
    - Improvements
    """

    review = llm.invoke(prompt).content

    return {
        "review": review
    }

# Final Node
def final_writer(state):

    prompt = f"""
    Create final answer.

    Research:
    {state['research']}

    Review:
    {state['review']}
    """

    final_answer = llm.invoke(prompt).content

    return {
        "final_answer": final_answer
    }

# Build Graph
builder = StateGraph(AgentState)

builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("critic", critic)
builder.add_node("final_writer", final_writer)

builder.set_entry_point("planner")

builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "critic")
builder.add_edge("critic", "final_writer")
builder.add_edge("final_writer", END)

graph = builder.compile()


import streamlit as st

st.set_page_config(
    page_title="DeepAgents AI",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 DeepAgents Research Assistant")
st.caption("Powered by LangGraph + Groq")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox(
        "Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant"
        ]
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.2
    )

    st.success("🟢 Ready")

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Agents", "4")

with col2:
    st.metric("Framework", "LangGraph")

with col3:
    st.metric("Status", "Active")

st.divider()

# User Input
query = st.text_area(
    "Research Topic",
    height=180,
    placeholder="Enter a research topic..."
)

# Generate
if st.button("🚀 Generate Report", use_container_width=True):

    with st.spinner("Agents are working..."):

        result = graph.invoke(
            {
                "query": query,
                "plan": "",
                "research": "",
                "review": "",
                "final_answer": ""
            }
        )

    st.session_state["result"] = result

# Results
if "result" in st.session_state:

    result = st.session_state["result"]

    tab1, tab2 = st.tabs(
        ["📄 Final Report", "📝 Agent Logs"]
    )

    with tab1:

        st.subheader("Final Research Report")

        st.write(result["final_answer"])

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "📥 Download TXT",
                data=result["final_answer"],
                file_name="research_report.txt",
                mime="text/plain"
            )

        with col2:
            st.download_button(
                "📥 Download Markdown",
                data=result["final_answer"],
                file_name="research_report.md",
                mime="text/markdown"
            )

    with tab2:

        st.subheader("Planner Output")
        st.write(result.get("plan", ""))

        st.subheader("Research Output")
        st.write(result.get("research", ""))

        st.subheader("Critic Output")
        st.write(result.get("review", ""))

st.divider()

st.caption(
    "DeepAgents • LangGraph • Groq • Multi-Agent Research System"
)