from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import Runnable
from app_agent.utils.chains.templates import (
    roll_template,
    classify_level_template,
    traduce_to_english_template,
    reasoning_template,
    traduce_answer_template,
)
from app_agent.utils.schemas.schemas import Language,parser_pydantic_language 


load_dotenv()

basic_llm = ChatOpenAI(model="gpt-5-mini")
advanced_llm = ChatOpenAI(model="gpt-5.2")

######### CHAIN 1: classify level
classify_level_prompt = ChatPromptTemplate.from_messages(
    [("system",classify_level_template),]
).partial(roll=roll_template)

classify_level_chain = classify_level_prompt | advanced_llm

########## CHAIN 2: TRADUCE QUERY

traduce_to_english_prompt = ChatPromptTemplate.from_messages(
    [("system",traduce_to_english_template),]
).partial(roll=roll_template)


traduce_to_english_chain = traduce_to_english_prompt|advanced_llm.bind_tools(
    tools=[Language],tool_choice="Language"
)|parser_pydantic_language

######### CHAIN 3: REASONING CHAIN

def reasoning_chain(llm:BaseChatModel) -> Runnable[dict,BaseMessage]:
    
    reasoning_prompt = ChatPromptTemplate.from_messages([
        ("system",reasoning_template),
        MessagesPlaceholder(variable_name="messages"),
    ]).partial(roll=roll_template)

    reasoning_chain = reasoning_prompt | llm
    
    return reasoning_chain


########## CHAIN 4: BACK TO THE ORIGINAL LANGUAGE

def back_original_language_chain(llm:BaseChatModel) -> Runnable[dict,BaseMessage]: 

    traduce_prompt = ChatPromptTemplate.from_messages(
        [("system",traduce_answer_template)]
    ).partial(roll=roll_template)

    traduce_chain = traduce_prompt | llm 

    return traduce_chain



if __name__=="__main__":
    print("testing ...")







