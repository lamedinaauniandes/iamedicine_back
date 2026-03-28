from pydantic import BaseModel,Field
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

class Language(BaseModel): 
    english_query: str = Field(description="English query")
    spanish_query: str = Field(description="Spanish query")
    init_language: str = Field(description="language of initial query")


parser_pydantic_language = PydanticToolsParser(tools=[Language])


if __name__ == "__main__":
    print("testing ... ")