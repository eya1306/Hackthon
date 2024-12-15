from langgraph.graph import END , StateGraph, MessagesState, START
from langchain_core.messages import convert_to_messages, RemoveMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.config import RunnableConfig
from .chains.chains import intent_recognition_chain, rephrase_chain, categorize_chain
from .vector_store.chroma_management import add_new_doc
import os
from dotenv import load_dotenv
load_dotenv()
import re

def clean_newlines(input_string):
    # Remove all newline characters from the string
    cleaned_string = re.sub(r'\n', '', input_string)
    return cleaned_string


llmG = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", google_api_key=os.getenv("GOOGLE_API_KEY"))

class AgentState(MessagesState):
    """The state of the graph"""
    user_id:str
    message_id:str
    message_text :str
    summary_text : str
    current : str


def intent_recognition_node(state : AgentState):
    """"""
    print(f"The state in Intent {state}")
    intent_recognition_runnable = intent_recognition_chain(llm=llmG)
    result = intent_recognition_runnable.invoke({"user_input": state["messages"][-1].content})

    return {"messages": [result], "current": "Intent"}


def check_message_node(state: AgentState):
    """Check if the user's message message exist"""
    print(f"The state in Check {state}")
    result = add_new_doc(state["user_id"], state["message_id"], state["message_text"])
    print(result)
    return {"messages":[result], "current":"Check Message"}

def rephrase_node(state : AgentState):
    print(f"The state in rephrase {state}")

    rephrase_runnable = rephrase_chain(llm=llmG)
    result = rephrase_runnable.invoke({"user_input": state["message_text"]})
    return {"messages":[result], "current":"Rephrase"}

def categorize_node(state : AgentState):
    print(f"The state in rephrase {state}")

    categorize_runnable = categorize_chain(llm=llmG)
    result = categorize_runnable.invoke({"user_input": state["message_text"], "summary":state["messages"][-1].content})
    return {"messages":[result], "current":"Categorize", "summary_text":state["messages"][-1].content}

def if_complaint(state:AgentState):
    result = state["messages"][-1].content
    clean=clean_newlines(result)
    print(f"clean {clean}")
    if clean == "True":
        return "check"
    else:
        return END
    
def if_msg_exist(state:AgentState):
    result = state["messages"][-1].content
    clean=clean_newlines(result)
    print(f"clean {clean}")
    if clean == "added":
        return "rephrase"
    else:
        return END

workflow = StateGraph(AgentState)

workflow.add_node("intent", intent_recognition_node)
workflow.add_node("check", check_message_node)
workflow.add_node("rephrase", rephrase_node)
workflow.add_node("categorize", categorize_node)

workflow.add_edge(START, "intent")
workflow.add_conditional_edges("intent",if_complaint, {
    "check":"check",
    END:END
})
workflow.add_conditional_edges("check", if_msg_exist, {
    "rephrase":"rephrase",
    END : END
})

workflow.add_edge("rephrase", "categorize")


graph = workflow.compile()

