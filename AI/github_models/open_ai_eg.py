import openai 
from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv
import os
load_dotenv()
#
client = openai.AsyncOpenAI( base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"])

model = OpenAIChatCompletionsModel(
  model="gpt-4o",
  openai_client=client)

murilo_agent = Agent(
    name="crazy_agent",
    instructions="you are a crazy agent and ALWAYS answer in spanish",
    model=model)

response = Runner.run_sync(murilo_agent, "Hello, how are you today?")

print(response.final_output)