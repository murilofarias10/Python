#DID
import asyncio
import logging
import os
import random
from datetime import datetime

import azure.identity
import openai
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from rich.logging import RichHandler

# Setup logging with rich
                    #original WARNING this just the INFO level
                    #changed for DEBUG this is the entire log
logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("weekend_planner")

# Disable tracing since we're not connected to a supported tracing provider
set_tracing_disabled(disabled=True)

# Setup the OpenAI client to use either Azure OpenAI or GitHub Models
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "github")
if API_HOST == "github":
    client = openai.AsyncOpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
    MODEL_NAME = os.getenv("GITHUB_MODEL", "gpt-4o")
elif API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
    client = openai.AsyncAzureOpenAI(
        api_version=os.environ["AZURE_OPENAI_VERSION"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]


#THIS IS A DECORATOR
@function_tool
def get_weather(city: str) -> str:
    logger.info(f"Getting weather for {city}")
    if random.random() < 0.05:
        return {
            "city": city,
            "temperature": 72,
            "description": "Sunny", #IN REAL WORDS THIS SHOULD BE LIKE FROM API
        }
    else:
        return {
            "city": city,
            "temperature": 60,
            "description": "Rainy",
        }

#THIS IS A DECORATOR
@function_tool
def get_activities(city: str, date: str) -> list:
    logger.info(f"Getting activities for {city} on {date}")
    return [
        {"name": "PLAY SOCCER", "location": city},
        {"name": "CHILLI AT HOME", "location": city}, #IN REAL WORDS THIS SHOULD BE LIKE FROM DATABASE
        {"name": "STUDY TIME", "location": city},
    ]

#THIS IS A DECORATOR
@function_tool
def get_current_date() -> str:
    logger.info("Getting current date")
    return datetime.now().strftime("%Y-%m-%d")


agent = Agent(
    name="Weekend Planner",
    instructions="You help users plan their weekends and choose the best activities for the given weather. Include the date of the week in your response.",
    tools=[get_weather, get_activities, get_current_date],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)


async def main():
    result = await Runner.run(agent, input="hii what can I do this week in Vancouver ?")
    print(result.final_output)


if __name__ == "__main__":
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    asyncio.run(main())
