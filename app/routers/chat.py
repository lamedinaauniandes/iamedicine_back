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
from langgraph.checkpoint.memory import InMemorySaver 
import json

router = APIRouter(
    prefix="/chat",
    tags=['login']
)

agent = None


@router.on_event("startup")
def startup():
    global agent
    checkpointer = InMemorySaver()
    agent = state_machine.compile(checkpointer = checkpointer)

@router.post("",response_model=ChatResponse)
async def chat(req:ChatRequest,db:Session = Depends(get_db),current_user:User=Depends(get_current_user)):
    if agent is None: 
        raise HTTPException(status_code=400,detail="Agent not initialized")
    message_user = req.message.strip()
    if not message_user:
        raise HTTPException(status_code=400,detail="empty message")
    try:
        res = await run_in_threadpool(
            agent.invoke,
            {
                "messages": [HumanMessage(content=message_user)],
                "retry":0,
                "image_url":"",
                "english_query":"",
                "spanish_query":"",
                "image_description":""
            },
            config={
                "configurable": {
                    "thread_id": current_user
                }
            }
            
        )

        print("-"*50,"Agent Response")
        # print(json.dumps(res, indent=4, ensure_ascii=False, default=str))

        msgs = res.get("messages",[])
        url_image = res.get("image_url","")
    
        if not msgs:
            raise RuntimeError("Agent returned no messages")
        
       
        answer = getattr(msgs[-1],"content",None) or str(msgs[-1])

        print("url_image: ",url_image)
        return ChatResponse(reply=answer,url_image=url_image)

    except Exception as e:
        print("debug 8",f" {e}")
        raise HTTPException(status_code=500,detail="chat processing failed")

        
