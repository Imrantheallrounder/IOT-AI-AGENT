import asyncio
import logging
from publisher import MQTTPublisher
from transcribe import transcribe_audio
from pydantic_structure import GeneralInfoEvent, QueryIntent, DevicesAction, TakeActionEvent        # QueryIdentificationEvent
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
from devices.loader import load_devices_from_yaml

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALL_DEVICES = load_devices_from_yaml()
DEBUG = False

mqtt_publisher = MQTTPublisher("localhost", 1883)

class MainWorkflow(Workflow):    
    MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-2.5-flash")
    llm = GoogleGenerativeAI(model=MODEL_NAME)

    @step
    async def identify_query_intent(self, ev: StartEvent) -> Union[StopEvent, TakeActionEvent, GeneralInfoEvent]:
        user_query = ev.query
        parser = JsonOutputParser(pydantic_object=QueryIntent)
        prompt_template = PromptTemplate(
            template=PROMPT_QUERY_IDENTIFICATION,
            input_variables=["user_query"],
            partial_variables={"format_instructions":parser.get_format_instructions()})
        chain = prompt_template | self.llm | parser
        query = {"user_query":user_query}
        response = await chain.ainvoke(query)
        # logger.info(f"Intent response: {response}")
        if response.get("action"):
            if DEBUG:
                logger.info("Action identified")
            return TakeActionEvent(query=user_query)
        elif response.get("general"):
            if DEBUG:
                logger.info("General query identified")
            return GeneralInfoEvent(query=user_query)
        elif response["restricted"]:
            return StopEvent(result="Restricted query identified. Please try again with a different query.")
        else:
            return StopEvent(result="No event identified. Please try again.")

    @step
    async def take_action(self, ev: TakeActionEvent) -> StopEvent:
        user_query = ev.query
        parser = JsonOutputParser(pydantic_object=DevicesAction)
        prompt_template = PromptTemplate(
            template=PROMPT_ACTION,
            input_variables=["user_query"],
            partial_variables={"format_instructions":parser.get_format_instructions(), "devices_info":ALL_DEVICES})
        chain = prompt_template | self.llm | parser
        query = {"user_query":user_query}
        response = await chain.ainvoke(query)
        # print("#"*100)
        # logger.info(f"Action response: {response}")
        tasks = []
        for item in response.get('devices'):
            topic = item.get('device_id')
            # payload = {'state': item.get('state')}
            payload = item.get('state')
            if DEBUG:
                logger.info(f"Publishing to topic: {topic}, |  Payload: {payload}")
            logger.info(f"Publishing to topic: {topic}, |  Payload: {payload}")
            tasks.append(mqtt_publisher.publish(topic, payload))
        await asyncio.gather(*tasks)
        return StopEvent(result=response)
    
    @step
    async def answer_general_query(self, ev: GeneralInfoEvent) -> StopEvent:
        user_query = ev.query
        prompt_template = PromptTemplate(
            template="You are an AI assistant. Your response will be used as audio response, Answer the user query in concise manner. user query: {query}",
            input_variables=["query"]
        )
        chain = prompt_template | self.llm
        query = {"query": user_query}
        response = await chain.ainvoke(query)
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
        # if DEBUG:
        #     logger.info(f"Workflow output: {out}")
    except Exception as e:
        logger.exception(f"Error during workflow execution: {e}")

async def main():
    while True:
        await listen_for_wake_word(on_detected=handle_wakeword)

if __name__=="__main__":
    asyncio.run(main())