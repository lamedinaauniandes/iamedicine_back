from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from app_agent.utils.chains.chains import (
    reasoning_chain,
    classify_level_chain,
    traduce_to_english_chain,
    back_original_language_chain,
)
from app_agent.utils.tools.tool_rag import retrieve_context

basic_llm = ChatOpenAI(model="gpt-5-mini")   ### models would be in config
advanced_llm = ChatOpenAI(model="gpt-5.2")
tools = [retrieve_context]

#### state object
class MessageGraph(TypedDict): 
    messages: Annotated[list[BaseMessage],add_messages]
    english_messages: Annotated[list[BaseMessage],add_messages]
    init_language: str 
    level:str 
    llm: BaseChatModel


def traduce_query_node(state:MessageGraph):
    print("-"*50,"traduce_query_node") 
    response = traduce_to_english_chain.invoke({
        "query": state["messages"][-1]
    })
    return {
        "init_language":response[-1].init_language, 
        "english_message":response[-1].english_query
        }

def classify_level_node(state:MessageGraph):
    print("-"*50,"classify_level_node")
    response = classify_level_chain.invoke({ 
        "query": state["messages"][-1]
    })
    return {"level":response.content}


def assign_llm_node(state:MessageGraph):
    print("-"*50,"assign_llm_node")
    if state["level"] == "student": 
        return {"llm":basic_llm.bind_tools(tools)}
    return {"llm":advanced_llm.bind_tools(tools)}


def reasoning_node(state:MessageGraph):
    print("-"*50,"reasoning_node") 
    reasoning_motor = reasoning_chain(state["llm"])
    response = reasoning_motor.invoke({
        "messages":state["english_messages"]
    })
    return {"english_messages":[response]}

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
    