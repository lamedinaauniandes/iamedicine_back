## app libraries
from fastapi import (
    APIRouter, 
    HTTPException, 
)
from fastapi.concurrency import run_in_threadpool

#### schemas & tools
from app.schemas import ChatRequest,ChatResponse
from app.tools import (
    dynamic_model_selection,
    retrieve_content, 
    basic_model, 
)

#### langchain
from langchain.agents import create_agent


router = APIRouter()


#### env variable
SYSTEM_PROMPT = """You are an expert rheumatologist in joint examination in adult patients with rheumatoid arthritis.
You have access to a tool that retrieves relevant documentation.
Use the tool to find relevant information before answering the question.
Always cite the sources you use in your answers.
If you cannot find the answer in the retrieved documentation, say so.
No suggestions—just answer.
"""

agent = None

@router.on_event("startup")
def startup():
    global agent
    agent = create_agent(
        model=basic_model,
        tools=[retrieve_content],
        system_prompt=SYSTEM_PROMPT,
    )

@router.post("",response_model=ChatResponse)
async def chat(req:ChatRequest): 
    
    if agent is None: 
        raise HTTPException(status_code=400,detail="Agent not initialized")
    
    message_user = req.message.strip()
    if not message_user:
        raise HTTPException(status_code=400,detail="empty message")
    
    try: 
        res = await run_in_threadpool(
            agent.invoke, 
            {"messages":[{"role":"user","content":message_user}]}
        )
        msgs = res.get("messages",[])
        if not msgs: 
            raise RuntimeError("Agent returned no messages")
        
        answer = getattr(msgs[-1],"content",None)  or str(msgs[-1])
        
        return ChatResponse(reply=answer)

    except Exception as e: 
        raise HTTPException(status_code=500,detail="chat processing failed")