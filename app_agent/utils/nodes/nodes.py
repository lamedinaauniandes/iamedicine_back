from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,ToolMessage,HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from app_agent.utils.chains.chains import (
    exclusion_criteria_chain,
    out_scope_manage_chain,
    classify_level_chain,
    traduce_to_english_chain,
    reasoning_chain,
    select_image_chain,
    back_original_language_chain,
)
from app_agent.utils.chains.templates import clasification_user
from app_agent.utils.tools.tool_rag import retrieve_context
from langgraph.graph import StateGraph,START,END
from app_agent.utils.nodes.node_names import (
    OUT_SCOPE_MANAGE_NODE,
    EXCLUSION_CRITERIA_NODE,
    TRADUCE_QUERY_NODE,
    CLASSIFY_LEVEL_NODE,
    ASSIGN_LLM_NODE,
    REASONING_NODE,
    RAG_NODE,
    SELECT_IMAGE_NODE,
    TRADUCE_ORIGINALLANGUAGE_NODE,
)
from langgraph.graph import StateGraph,START,END

basic_llm = ChatOpenAI(model="gpt-5-mini")   ### models would be in config
advanced_llm = ChatOpenAI(model="gpt-5.2")
tools = [retrieve_context]

RETRIES_MAX = 2    #### maximum retries for each node

#### state object
class MessageGraph(TypedDict): 
    messages: Annotated[list[BaseMessage],add_messages]
    english_messages: Annotated[list[BaseMessage],add_messages]
    init_language:str
    english_query: str
    spanish_query: str
    level: str
    llm: BaseChatModel
    query: str
    scope: str
    retry: int = 0
    image_url: str
    image_description: str

def exclusion_criteria_node(state:MessageGraph): 
    print("-"*50,"exclusion_criteria_node")
    # print(f"debug 0 : {state["messages"][-1]}")
    response = exclusion_criteria_chain.invoke({
        "messages":state["messages"],
        "query":state["messages"][-1]
    }) 
    return {"scope":response.content,"retry":state["retry"] + 1 }

def exclusion_criteria_edge(state:MessageGraph): 
    print("-"*50,"exclusion_criteria_edge")

    scope = state["scope"].upper().replace(" ","")
    retry = state["retry"]

    # print("#"*10,f"scope: {state['scope']}")
  
    if scope == "OUT_SCOPE" and retry>RETRIES_MAX:
        return OUT_SCOPE_MANAGE_NODE
    elif scope == "OUT_SCOPE" and retry<=RETRIES_MAX:
        return EXCLUSION_CRITERIA_NODE

    return TRADUCE_QUERY_NODE

def out_scope_manage_node(state:MessageGraph): 
    print("-"*50,"out_scope_manage_node")
    response = out_scope_manage_chain.invoke({
        "messages":state["messages"]
    })
    return {"messages":[response]}  

def traduce_query_node(state:MessageGraph):
    print("-"*50,"traduce_query_node") 
    response = traduce_to_english_chain.invoke({
        "messages": state["messages"]
    })
    return {
        "english_messages":HumanMessage(content=response[-1].english_query),
        "init_language":response[-1].init_language,
        "english_query":response[-1].english_query,
        "spanish_query":response[-1].spanish_query
        }

def classify_level_node(state:MessageGraph):
    print("-"*50,"classify_level_node")
    response = classify_level_chain.invoke({ 
        "messages": state["messages"]
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
        "messages": state["english_messages"],
        "level": clasification_user[state["level"]],
        "query": state["english_query"],
        "spanish_query":state["spanish_query"],
    })
    return {"english_messages":[response]}

def should_investigate_edge(state:MessageGraph) -> str: 
    print("-"*50,"should investigate....")
    # print("-"*50,state["english_messages"][-1].tool_calls)
    if state["english_messages"][-1].tool_calls: 
        return RAG_NODE
    if state["english_messages"][-1].content == "The requested information is not found in the reference documentation.":
        return TRADUCE_ORIGINALLANGUAGE_NODE
    return SELECT_IMAGE_NODE

def select_image_node(state:MessageGraph) -> str: 
    print("-"*50,"select_image_node")

    selectimage_motor = select_image_chain(state["llm"])

    response = selectimage_motor.invoke({
        "answer":state["english_messages"][-1].content
    })

    return { 
      "image_url": response[-1].image_url,
      "image_description": response[-1].description
    }


def traduce_original_language(state:MessageGraph):
    print("-"*50,"traduce_original_language") 
    print(state["english_messages"][-1].content)
    if state["init_language"].lower().replace(" ","") != "english":
        traduce_motor = back_original_language_chain(state["llm"])
        re = traduce_motor.invoke({
            "language": state["init_language"],
            "answer": state["english_messages"][-1].content
        })
        return {"messages":re}    
    return {"messages":[state["english_messages"][-1]]}


tool_node = ToolNode(tools,messages_key="english_messages")

if __name__ == "__main__":
    print("testing...")
    