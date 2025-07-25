import asyncio
import logging
from utility import utility
from transcribe import transcribe_audio
from pydantic_structure import GeneralInfoEvent, QueryIntent, ApplianceAction, TakeActionEvent        # QueryIdentificationEvent
from prompts import PROMPT_QUERY_IDENTIFICATION, PROMPT_ACTION
from dotenv import load_dotenv
from wakeword.wakeword_detection import listen_for_wake_word
from llama_index.core.workflow import (StartEvent, StopEvent, step, Workflow)
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from typing import Union
import os
from sounds import play_chime

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MainWorkflow(Workflow):    
    MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
    llm = GoogleGenerativeAI(model=MODEL_NAME)

    @step
    def identify_query_intent(self, ev: StartEvent) -> Union[StopEvent, TakeActionEvent, GeneralInfoEvent]:
        user_query = ev.query
        parser = JsonOutputParser(pydantic_object=QueryIntent)
        prompt_template = PromptTemplate(
            template=PROMPT_QUERY_IDENTIFICATION,
            input_variables=["user_query"],
            partial_variables={"format_instructions":parser.get_format_instructions()})
        chain = prompt_template | self.llm | parser
        query = {"user_query":user_query}
        response = chain.invoke(query)
        # logger.info(f"Intent response: {response}")
        if response.get("action"):
            logger.info("Action identified")
            return TakeActionEvent(query=user_query)
        elif response.get("general"):
            logger.info("General query identified")
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
        # logger.info(f"Action response: {response}")
        topic, msg = utility.get_topic_msg(response)
        logger.info(f"Publishing to topic: {topic}, message: {msg}")
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

async def handle_wakeword(keyword):
    logger.info(f"Wake word '{keyword}' detected. Starting workflow.")
    play_chime()
    try:
        w = MainWorkflow(timeout=60, verbose=False)
        query = await asyncio.to_thread(transcribe_audio)
        if not query:
            logger.warning("No valid query found.")
            return
        out = await w.run(query=query)
        logger.info(f"Workflow output: {out}")
    except Exception as e:
        logger.exception(f"Error during workflow execution: {e}")

async def main():
    while True:
        await listen_for_wake_word(on_detected=handle_wakeword)

if __name__=="__main__":
    asyncio.run(main())


# device_info = {
#     'device_name': 'light bulb',
#     'device_id': 'bulb-001',
#     'device_description': 'a light bulb that can be turned on or off',
#     'device_location': 'bedroom_a',
#     'device_version': '1.0',
# }