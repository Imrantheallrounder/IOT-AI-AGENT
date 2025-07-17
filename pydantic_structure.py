# from langchain.pydantic_v1 import BaseModel, Field
from pydantic import BaseModel, Field
from llama_index.core.workflow import  Event

class QueryIdentificationEvent(Event):
    query: str
    type: str

class TakeActionEvent(Event):
    query: str

class QueryIntent(BaseModel):
    # casual: bool = Field(description="When the user is asking a casual question or is greeting")
    restricted: bool = Field(description="When the user asks a sensitive information that may be harmful")
    general: bool = Field(description="When the user needs information/knowledge about any topic")
    action: bool = Field(description="When the user is giving order to do something")

class ApplianceAction(BaseModel):
    floor: int = Field(description="Identify which floor is mentioned by the user. There are 3 floors: ground floor, 1st floor and 2nd floor. return 0 for ground floor, 1 for 1st floor, 2 for 2nd floor.")
    space: str = Field(description="Identify which area or space the user is referring to. There are various areas: bedroom_a, bedroom_b, master_bedroom, balcony, kitchen, dinning_hall, living_room, bathroom.")
    appliance: str = Field(description="Identify the appliance name. There are various appliances: light, fan, ac,")
    state: str = Field(description="Identify whether user wants to turn the appliance on or off.")
    response: str = Field(description="Prepare a concise response to the user query")