import os
from logger import get_logger
from dotenv import load_dotenv
from langchain.llms import OpenAI

load_dotenv()
OPEN_AI_TOKEN = os.environ.get("OPEN_AI_TOKEN")

# logger
logger = get_logger(__name__)
logger.info("Starting Langchain")

llm_open_ai = OpenAI(model="text-davinci-003", openai_api_key=OPEN_AI_TOKEN)

# Completion handlers
def open_ai_llm_completion_handler(prompt):
    completion_open_ai = llm_open_ai(prompt)
    logger.info("Completion OpenAI: %s", completion_open_ai)
    return completion_open_ai