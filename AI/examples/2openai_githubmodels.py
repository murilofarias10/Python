#Did
import os

from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    base_url="https://models.inference.ai.azure.com", #this is an endpoint
    api_key=os.environ["GITHUB_TOKEN"],
)
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful analyst.",
        },
        {
            "role": "user",
            "content": "I would like to know about tokens and costs?",
        },
    ],
    model=os.getenv("GITHUB_MODEL", "gpt-4o"),
)
print(response.choices[0].message.content)
