from llama_index.core.workflow import (StartEvent, StopEvent, step, Workflow)
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from typing import Union
import os

from utility import utility
from pydantic_structure import QueryIntent, ApplianceAction, QueryIdentificationEvent, TakeActionEvent
from prompts import PROMPT_QUERY_IDENTIFICATION, PROMPT_ACTION
from dotenv import load_dotenv
load_dotenv()

class MainWorkflow(Workflow):    
    MODEL_NAME = "gemini-2.0-flash"
    llm = GoogleGenerativeAI(model=MODEL_NAME)

    @step
    def identify_query_intent(self, ev: StartEvent) -> Union[StopEvent, TakeActionEvent]:  # | GeneralInfoEvent | RestrictedEvent:
        user_query = ev.query

        parser = JsonOutputParser(pydantic_object=QueryIntent)
        prompt_template = PromptTemplate(
            template=PROMPT_QUERY_IDENTIFICATION,
            input_variables=["user_query"],
            partial_variables={"format_instructions":parser.get_format_instructions()})

        chain = prompt_template | self.llm | parser

        query = {"user_query":user_query}
        response = chain.invoke(query)
        print(f"resp1: {response}")
        if response["action"]:
            return TakeActionEvent(query=user_query)
        # elif response["general"]:
        #     return GeneralInfoEvent()
        # elif response["restricted"]:
        #     return RestrictedEvent()
        else:
            return "Try Again, The query is not identified properly"
        
        return StopEvent(query_intent=response)

    @step
    def take_action(self, ev: TakeActionEvent) -> StopEvent:
        user_query = ev.query

        parser = JsonOutputParser(pydantic_object=ApplianceAction)
        prompt_template = PromptTemplate(
            template=PROMPT_ACTION,
            input_variables=["user_query"],
            partial_variables={"format_instructions":parser.get_format_instructions()})

        chain = prompt_template | self.llm | parser

        query = {"user_query":user_query}
        response = chain.invoke(query)
        print(f"resp2: {response}")
        
        topic, msg = utility.get_topic_msg(response)
        print(topic, msg)
        
        utility.publish_message(str(topic), str(msg))
        
        return StopEvent(result=response)

    # @step
    # def deny_response():
    #     pass

    # @step
    # def answer_general_query():
    #     pass
    
import asyncio
async def main():
	w = MainWorkflow(timeout=60, verbose=False)
	out = await w.run(query="Turn on led 1 in room A")
	print(out)

if __name__=="__main__":
	asyncio.run(main())
