# from langchain.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field
from llama_index.core.workflow import  Event
from typing import List

# class QueryIdentificationEvent(Event):
#     query: str
#     type: str

class TakeActionEvent(Event):
    query: str

class GeneralInfoEvent(Event):
    query: str

class QueryIntent(BaseModel):
    # casual: bool = Field(description="When the user is asking a casual question or is greeting")
    restricted: bool = Field(description="When the user asks a sensitive information that may be harmful")
    general: bool = Field(description="When the user needs information/knowledge about any topic")
    action: bool = Field(description="When the user is giving order to do something")

class ApplianceAction(BaseModel):
    device_id: str = Field(description="Identify the device id.")
    state: str = Field(description="Identify whether user wants to turn the device on or off. (on | off)")

class DevicesAction(BaseModel):
    devices: List[ApplianceAction]
    response: str = Field(description="Prepare a concise response to the user query")