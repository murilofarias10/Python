import asyncio
import os

import azure.identity
import openai
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from agents.extensions.visualization import draw_graph
from dotenv import load_dotenv

# Disable tracing since we're not using OpenAI.com models
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

@function_tool
def get_weather(city: str) -> str:
    return {
        "city": city,
        "temperature": 72,
        "description": "Sunny",
    }

japanese_agent = Agent(
    name="japanese agent",
    instructions="You only speak Japanese.",
    tools=[get_weather],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

portuguese_agent = Agent(
    name="portuguese agent",
    instructions="You only speak Portuguese",
    tools=[get_weather],
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[japanese_agent, portuguese_agent], #to delegate to other agents
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
)

async def main():
    result = await Runner.run(triage_agent, input="I would like to know the weather in Vancouver, feel free to select which language you think is better to respond.")
    gz_source = draw_graph(triage_agent, filename="openai_agents_handoffs.png")
    
    # save graph to file in graphviz format
    #gz_source.save("openai_agents_handoffs.dot")

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
