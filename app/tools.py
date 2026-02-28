import os 
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import (
    wrap_model_call,
    ModelRequest, 
    ModelResponse,
)
from langchain_core.prompts import PromptTemplate
from  langchain.messages import SystemMessage,HumanMessage,AIMessage 
from langchain.tools import tool
from langchain_pinecone import PineconeVectorStore 
from langchain_openai import OpenAIEmbeddings, ChatOpenAI 
from dotenv import load_dotenv

load_dotenv(override=True)

classifier_model = ChatOpenAI(model="gpt-5-mini")
basic_model = ChatOpenAI(model="gpt-5-mini")
advanced_model = ChatOpenAI(model="gpt-5.2")


embeddings = OpenAIEmbeddings(
    model = os.getenv("MODEL_EMBEDDINGS"),
    dimensions = int(os.getenv("DIMENSION_EMBEDDINGS")),
)

vectorstore = PineconeVectorStore(
    index_name= os.getenv("INDEX_NAME"), 
    embedding = embeddings,
)

@wrap_model_call
def dynamic_model_selection(request:ModelRequest,handler) -> ModelResponse: 
    "Choose model based on conversation complexity"

    template = """You are an expert rheumatologist specialized in joint examination in adult patients with rheumatoid arthritis.
    Classify the query below as either "student" or "expert". A "student" is a resident in a health-related program, 
    and an "expert" is a postgraduate student.
    Respond with exactly one of these two words and nothing else.

    {query}
    """
    query_user = request.state["messages"][0].content

    prompt_template = PromptTemplate(
        input_variables=["query"],
        template=template
    )

    prompt_query = prompt_template.format(query=query_user)
    res = classifier_model.invoke(prompt_query)

    label = res.content.strip().lower()

    if label=="student":
        model = basic_model
    else:
        model = advanced_model

    return handler(request.override(model=model))
 



@tool(response_format="content_and_artifact")
def retrieve_content(query:str):
    """Retrieve relevant documentation to help answer user queries about rheumatologist."""

    retrieved_docs = vectorstore.as_retriever().invoke(query,k=4)

    serialized = "\n\n".join(
        (f"Source: {doc.metadata.get("source","Unknown")} \n\n content {doc.page_content}")
        for doc in retrieved_docs
    )

    return serialized, retrieved_docs



if __name__=="__main__":
    print("deubug 1")

