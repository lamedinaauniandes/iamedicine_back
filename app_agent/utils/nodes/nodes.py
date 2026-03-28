from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from app_agent.utils.chains.chains import (
    reasoning_chain,
    exclusion_criteria_chain,
    out_scope_manage_chain,
    classify_level_chain,
    traduce_to_english_chain,
    back_original_language_chain,
)
from app_agent.utils.chains.templates import clasification_user
from app_agent.utils.tools.tool_rag import retrieve_context
from langgraph.graph import StateGraph,START,END
from app_agent.utils.nodes.node_names import (
    OUT_SCOPE_MANAGE_NODE,
    TRADUCE_QUERY_NODE,
    CLASSIFY_LEVEL_NODE,
    ASSIGN_LLM_NODE,
    REASONING_NODE,
    RAG_NODE,
    TRADUCE_ORIGINALLANGUAGE_NODE,
)
from langgraph.graph import StateGraph,START,END

basic_llm = ChatOpenAI(model="gpt-5-mini")   ### models would be in config
advanced_llm = ChatOpenAI(model="gpt-5.2")
tools = [retrieve_context]

#### state object
class MessageGraph(TypedDict): 
    messages: Annotated[list[BaseMessage],add_messages]
    english_messages: Annotated[list[BaseMessage],add_messages]
    init_language:str
    level: str
    llm: BaseChatModel
    query: str
    english_query: str
    spanish_query: str
    scope: str

def exclusion_criteria_node(state:MessageGraph): 
    print("-"*50,"exclusion_criteria_node")
    response = exclusion_criteria_chain.invoke({
        "query":state["messages"][0]
    }) 
    return {"scope":response.content}

def exclusion_criteria_edge(state:MessageGraph): 
    print("-"*50,"exclusion_criteria_edge")
    if state["scope"].upper().replace(" ","") == "OUT_SCOPE":
        return OUT_SCOPE_MANAGE_NODE
    return TRADUCE_QUERY_NODE

def out_scope_manage_node(state:MessageGraph): 
    print("-"*50,"out_scope_manage_node")
    response = out_scope_manage_chain.invoke({
        "query":state["messages"][0]
    })
    return {"messages":response.content}

def traduce_query_node(state:MessageGraph):
    print("-"*50,"traduce_query_node") 
    response = traduce_to_english_chain.invoke({
        "query": state["messages"][0]
    })
    return {
        "init_language":response[-1].init_language,
        "english_messages":response[-1].english_query,
        "english_query":response[-1].english_query,
        "spanish_query":response[-1].spanish_query
        }

def classify_level_node(state:MessageGraph):
    print("-"*50,"classify_level_node")
    response = classify_level_chain.invoke({ 
        "query": state["english_query"]
    })
    return {"level":response.content}


def assign_llm_node(state:MessageGraph):
    print("-"*50,"assign_llm_node")
    if state["level"].replace(" ","").upper() == "STUDENT": 
        return {"llm":basic_llm.bind_tools(tools)}
    return {"llm":advanced_llm.bind_tools(tools)}


def reasoning_node(state:MessageGraph):
    print("-"*50,"reasoning_node") 
    reasoning_motor = reasoning_chain(state["llm"])
    response = reasoning_motor.invoke({
        "level": clasification_user[state["level"]],
        "messages":state["english_messages"],
        "query": state["english_query"],
        "spanish_query":state["spanish_query"],
    })
    return {"english_messages":[response]}

def should_investigate_edge(state:MessageGraph) -> str: 
    if state["english_messages"][-1].tool_calls: 
        return RAG_NODE
    return TRADUCE_ORIGINALLANGUAGE_NODE

def traduce_original_language(state:MessageGraph):
    print("-"*50,"traduce_original_language") 
    if state["init_language"].lower().replace(" ","") != "english":
        traduce_motor = back_original_language_chain(state["llm"])
        re = traduce_motor.invoke({
            "language": state["init_language"],
            "answer": state["english_messages"][-1].content
        })
        return {"messages":re}    
    return {"messages":state["english_messages"][-1]}


tool_node = ToolNode(tools,messages_key="english_messages")

if __name__ == "__main__":
    print("testing...")
    