from app_agent.utils.nodes.node_names import *
from langgraph.graph import StateGraph,START,END
from app_agent.utils.nodes.nodes import (
    MessageGraph,
    exclusion_criteria_node, ## !!! 
    exclusion_criteria_edge, ## !!! 
    out_scope_manage_node, ## !!! 
    traduce_query_node,
    classify_level_node, 
    assign_llm_node,
    reasoning_node,
    select_image_node,
    should_investigate_edge,
    traduce_original_language,
    tool_node,
) 


state_machine = StateGraph(MessageGraph)

state_machine.add_node(EXCLUSION_CRITERIA_NODE,exclusion_criteria_node)
state_machine.add_node(OUT_SCOPE_MANAGE_NODE,out_scope_manage_node)
state_machine.add_node(TRADUCE_QUERY_NODE,traduce_query_node)
state_machine.add_node(CLASSIFY_LEVEL_NODE,classify_level_node)
state_machine.add_node(ASSIGN_LLM_NODE,assign_llm_node)
state_machine.add_node(REASONING_NODE,reasoning_node)
state_machine.add_node(SELECT_IMAGE_NODE,select_image_node)
state_machine.add_node(RAG_NODE,tool_node)
state_machine.add_node(TRADUCE_ORIGINALLANGUAGE_NODE,traduce_original_language)

state_machine.add_edge(START,EXCLUSION_CRITERIA_NODE)
state_machine.add_conditional_edges(
    EXCLUSION_CRITERIA_NODE,
    exclusion_criteria_edge,
    [TRADUCE_QUERY_NODE,OUT_SCOPE_MANAGE_NODE,EXCLUSION_CRITERIA_NODE]
)
state_machine.add_edge(OUT_SCOPE_MANAGE_NODE,END)
state_machine.add_edge(TRADUCE_QUERY_NODE,CLASSIFY_LEVEL_NODE)
state_machine.add_edge(CLASSIFY_LEVEL_NODE,ASSIGN_LLM_NODE)
state_machine.add_edge(ASSIGN_LLM_NODE,REASONING_NODE)
state_machine.add_conditional_edges(
    REASONING_NODE, 
    should_investigate_edge,
    [RAG_NODE,SELECT_IMAGE_NODE]
)
state_machine.add_edge(RAG_NODE,REASONING_NODE)
state_machine.add_edge(SELECT_IMAGE_NODE,TRADUCE_ORIGINALLANGUAGE_NODE)
state_machine.add_edge(TRADUCE_ORIGINALLANGUAGE_NODE,END)

if __name__=="__main__":
    print("testing...")
    from langchain_core.messages import HumanMessage 
    agent = state_machine.compile()
    response = agent.invoke({
        "messages":HumanMessage(content="¿Que es la actividad de la enfermedad en la artritis reumatoide?")
    })
    print(response["messages"][-1].content)