import openai
from agents import Agent, OpenAIChatCompletionsModel, Runner
import os
from dotenv import load_dotenv
load_dotenv()

client = openai.AsyncOpenAI( base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"])

model = OpenAIChatCompletionsModel(
  model="gpt-4o",
  openai_client=client)

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
    model=model)

response = Runner.run_sync(spanish_agent, "Hello, how are you?")

print(response.final_output)