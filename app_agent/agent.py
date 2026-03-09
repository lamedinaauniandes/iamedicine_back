from app_agent.utils.nodes.nodes import (
    MessageGraph,
    traduce_query_node,
    classify_level_node, 
    assign_llm_node,
    reasoning_node,
    traduce_original_language,
    tool_node,
) 
from app_agent.utils.nodes.node_names import (
    TRADUCE_QUERY_NODE,
    CLASSIFY_LEVEL_NODE,
    ASSIGN_LLM_NODE,
    REASONING_NODE,
    RAG_NODE,
    TRADUCE_ORIGINALLANGUAGE_NODE,
)
from langgraph.graph import StateGraph,START,END


def should_investigate(state:MessageGraph) -> str: 
    if state["english_messages"][-1].tool_calls: 
        return RAG_NODE
    return TRADUCE_ORIGINALLANGUAGE_NODE


state_machine = StateGraph(MessageGraph)

state_machine.add_node(TRADUCE_QUERY_NODE,traduce_query_node)
state_machine.add_node(CLASSIFY_LEVEL_NODE,classify_level_node)
state_machine.add_node(ASSIGN_LLM_NODE,assign_llm_node)
state_machine.add_node(REASONING_NODE,reasoning_node)
state_machine.add_node(RAG_NODE,tool_node)
state_machine.add_node(TRADUCE_ORIGINALLANGUAGE_NODE,traduce_original_language)


state_machine.add_edge(START,TRADUCE_QUERY_NODE)
state_machine.add_edge(TRADUCE_QUERY_NODE,CLASSIFY_LEVEL_NODE)
state_machine.add_edge(CLASSIFY_LEVEL_NODE,ASSIGN_LLM_NODE)
state_machine.add_edge(ASSIGN_LLM_NODE,REASONING_NODE)
state_machine.add_conditional_edges(
    REASONING_NODE, 
    should_investigate,
    [RAG_NODE,TRADUCE_ORIGINALLANGUAGE_NODE]
)
state_machine.add_edge(RAG_NODE,REASONING_NODE)
state_machine.add_edge(TRADUCE_ORIGINALLANGUAGE_NODE,END)


# agent = state_machine.compile()



if __name__=="__main__":
    print("testing...")
    from langchain_core.messages import HumanMessage 
    response = agent.invoke({
        "messages":HumanMessage(content="¿Que es la actividad de la enfermedad en la artritis reumatoide?")
    })
    print(response["messages"][-1].content)