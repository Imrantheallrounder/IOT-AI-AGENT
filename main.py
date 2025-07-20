from llama_index.core.workflow import (StartEvent, StopEvent, step, Workflow)
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from typing import Union
import os

from utility import utility
from transcribe import transcribe_audio
from pydantic_structure import GeneralInfoEvent, QueryIntent, ApplianceAction, QueryIdentificationEvent, TakeActionEvent
from prompts import PROMPT_QUERY_IDENTIFICATION, PROMPT_ACTION
from dotenv import load_dotenv
load_dotenv()

from wakeword.wakeword_detection import listen_for_wake_word

class MainWorkflow(Workflow):    
    MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
    llm = GoogleGenerativeAI(model=MODEL_NAME)

    @step
    def identify_query_intent(self, ev: StartEvent) -> Union[StopEvent, TakeActionEvent, GeneralInfoEvent]:  # | GeneralInfoEvent | RestrictedEvent:
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
        if response.get("action"):
            print("Action identified")
            return TakeActionEvent(query=user_query)
        elif response.get("general"):
            print("General query identified")
            return GeneralInfoEvent(query=user_query)
        elif response["restricted"]:
            return StopEvent(result="Restricted query identified. Please try again with a different query.")
        else:
            return StopEvent(result="No event identified. Please try again.")

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
    
    @step
    def answer_general_query(self, ev: GeneralInfoEvent) -> StopEvent:
        user_query = ev.query

        prompt_template = PromptTemplate(
            template="You are an AI assistant. Your response will be used as audio response, Answer the user query in concise manner. user query: {query}",
            input_variables=["query"]
        )
        chain = prompt_template | self.llm
        query = {"query": user_query}
        response = chain.invoke(query)

        return StopEvent(result=response)

import asyncio
async def main():
    async def tmp_func():
        print("hello")
        w = MainWorkflow(timeout=60, verbose=False)
        query = transcribe_audio()
        # query = "Turn on the light in the living room on the first floor"
        if not query:
            print("No valid query found.")
            return
        out = await w.run(query=query)
        print(out)
    await listen_for_wake_word(on_detected=tmp_func)

if __name__=="__main__":
	asyncio.run(main())


# device_info = {
#     'device_name': 'light bulb',
#     'device_id': 'bulb-001',
#     'device_description': 'a light bulb that can be turned on or off',
#     'device_location': 'bedroom_a',
#     'device_version': '1.0',
# }