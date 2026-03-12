from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)
from fastapi.concurrency import run_in_threadpool
from app.oauth import get_current_user 
from app.db.database import get_db
from sqlalchemy.orm import Session 
from app.schemas import ChatRequest,ChatResponse, User, ShowUser, UpdateUser

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
async def chat(req:ChatRequest,db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    print("chat ...")
    if agent is None: 
        raise HTTPException(status_code=400,detail="Agent not initialized")
    print("debug 1")
    message_user = req.message.strip()
    print("debug 2")
    if not message_user:
        raise HTTPException(status_code=400,detail="empty message")
    print("debug 3")
    try:
        print("debug 4","\n", message_user)
        res = await run_in_threadpool(
            agent.invoke,
            {
                "messages": [HumanMessage(content=message_user)]
            }
        )

        print("debug 5 ")
        msgs = res.get("messages",[])

        if not msgs:
            print("debug 6")
            raise RuntimeError("Agent returned no messages")
        print("debug 7")
        answer = getattr(msgs[-1],"content",None) or str(msgs[-1])
        print("debug 7.1")
        print(answer)
        return ChatResponse(reply=answer)

    except Exception as e:
        print("debug 8",f" {e}")
        raise HTTPException(status_code=500,detail="chat processing failed")

        
