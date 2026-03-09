from fastapi import (
    APIRouter,
    HTTPException,
)
from fastapi.concurrency import run_in_threadpool
from app.schemas import ChatRequest,ChatResponse
from app_agent.agent import state_machine
from langchain_core.messages import HumanMessage

router = APIRouter(
    prefix="/chat",
    tags=['login']
)

agent = None


@router.on_event("startup")
def startup():
    global agent
    agent = state_machine.compile()

@router.post("",response_model=ChatResponse)
async def chat(req:ChatRequest):

    if agent is None: 
        raise HTTPException(status_code=400,detail="Agent not initialized")

    message_user = req.message.strip()

    if not message_user:
        raise HTTPException(status_code=400,detail="empty message"
        )

    try:
        res = await run_in_threadpool(
            agent.invoke({
                "messages":HummanMessage(content=message_user)
            })
        )

        msgs = res.get("messages",[])

        if not msgs:
            raise RuntimeError("Agent returned no messages")

        answer = getattr(msgs[-1],"content",None) or str(msgs[-1])

        return ChatResponse(reply=answer)

    except Exception as e:
        raise HTTPException(status_code=500,detail="chat processing failed")

        
