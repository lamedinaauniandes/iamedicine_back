from pydantic import BaseModel,Field
from langchain_core.output_parsers.openai_tools import PydanticToolsParser

class Language(BaseModel): 
    english_query: str = Field(description="English query")
    spanish_query: str = Field(description="Spanish query")
    init_language: str = Field(description="language of the conversation")


class Image(BaseModel):
    image_url: str = Field(
        # description="The URL of the image that best supports and enhances the response."
        description="The URL of the image"
    )
    description: str = Field(
        description="A description of the image."
    )


parser_pydantic_language = PydanticToolsParser(tools=[Language])
parser_pydantic_image = PydanticToolsParser(tools=[Image])

if __name__ == "__main__":
    print("testing ... ")