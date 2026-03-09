################### THIS CODE IF FOR EXAMPLE, THE AGENT CODE THERE IS IN ANOTHER REPOSITORY

# import os 
# from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import dynamic_model_selection,retrieve_content,basic_model
# from langchain.agents.middleware import (
#     wrap_model_call,
#     ModelRequest, 
#     ModelResponse,
# )
# from langchain_core.prompts import PrompTemplate
# from langchain.messages import HumanMessage, AIMessage 
from dotenv import load_dotenv

load_dotenv(override=True)


system_prompt = (
    "You are an expert rheumatologist in joint examination in adult patients with rheumatoid arthritis."
    "You have acces to a tool that retrieves relevant documentation."
    "Use the tool to find relevant information before answering question."
    "Always cite the sources you use in your answers."
    "if you cannot find the answer in the retrieved documentation, say so."
    "No suggestions—just answer."
)


agent = create_agent(
    model=basic_model,
    tools = [retrieve_content],
    middleware = [dynamic_model_selection],
    system_prompt=system_prompt 
)

res = agent.invoke({
    "messages":[
        {"role":"user","content":"Has the lack of a standardized physical joint examination been the main barrier to reliable assessment of rheumatoid arthritis disease activity, and does a consensus-based standardized protocol demonstrate that it is feasible, clinically superior, and significantly more accurate than non-standardized methods when validated against musculoskeletal ultrasound?"}
    ]
})


print(res)
print(res["messages"][-1].content)