import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_pinecone import PineconeVectorStore

from langchain_openai import (
    OpenAIEmbeddings
)


load_dotenv()

RETRIEVE_DOCS = 4 

embeddings = OpenAIEmbeddings(
    model = os.getenv("MODEL_EMBEDDINGS"),
    dimensions  = int(os.getenv("DIMENSION_EMBEDDINGS"))
)

vectorstore = PineconeVectorStore(
    index_name= os.getenv("INDEX_NAME"), 
    embedding = embeddings
)

@tool(response_format="content_and_artifact")
def retrieve_context(query:str): 
    """Retrieve relevant documentation to help answer queries about standarized examination in arthritis reumathoid"""
    print("*"*20,"retrieve tool\n",query)
    retrieve_docs = vectorstore.as_retriever().invoke(query,k=RETRIEVE_DOCS)

    serialized = "\n\n".join(
        (f"source {doc.metadata.get("source","unknow")} \n\n {doc.page_content} \n\n cite vancouver: {doc.metadata.get("vancouver_cite","Unknow")}")
        for doc in retrieve_docs
    )

    return serialized, retrieve_docs 


if __name__=="__main__":
    print("testing ....")
    query ="¿Que es la actividad de la enfemedad en la artritis reumatoide?"
    vectorstore.as_retriever.invoke(query,k=RETRIEVE_DOCS)

