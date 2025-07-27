from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import google.genai as genai
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

# from langchain_openai import ChatOpenAI
# openai_models = [model.id for model in OpenAI().models.list()]
groq_models = [model.id for model in Groq().models.list().data]
gemini_models = [m.name.replace("models/", "") for m in genai.Client().models.list()]

def create_llm(model_name: str, **kwargs):
    """
    Create an instance of llm from different llm provider with the specified model name.

    Args:
        model_name (str): The name of the model to use.
        **kwargs: Additional keyword arguments to pass to the llm constructor.

    Returns:
        llm: An instance of the specified llm configured with the provided parameters.
    """
    
    if model_name in groq_models:
        return ChatGroq(model=model_name, **kwargs)
    elif model_name in gemini_models:
        return ChatGoogleGenerativeAI(model=model_name, **kwargs)
    # elif model_name in openai_models:
    #     return ChatOpenAI(model_name=model_name, **kwargs)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")