"""
This is a MCP client that can be used to send text messages to phone numbers via Surge API.

To use it, you need to run the mcp_server.py file first.
Then, you can run this file to send text messages to phone numbers.
"""

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
import asyncio

transport = StreamableHttpTransport(url="http://0.0.0.0:8000/mcp")
client = Client(transport)


async def main(
    greet_name: str = "FastMCP 2.0", text_content: str = "Hello, how are you?"
):
    result_dict = {}
    # Connection is established here
    async with client:
        tools = await client.list_tools()
        print(f"\nAvailable tools: ")
        for i, tool in enumerate(tools):
            print(f"{i+1}. {tool.name}: {tool.description}")
            print("-" * 50)

        # Tool 1: run greet tool
        result = await client.call_tool("greet", {"text_content": greet_name})
        result_dict["greet"] = result[0].text

        # Tool 2: run textme tool
        result = await client.call_tool("textme", {"text_content": text_content})
        result_dict["textme"] = result[0].text

    # Print results
    print("\n\nOUTPUTS:")

    print("-" * 50)
    for j, (k, v) in enumerate(result_dict.items()):
        print(f"({j+1}) {k}:\n{v}\n")
    print()
    print("-" * 50)


if __name__ == "__main__":
    # Set the text content for the tools
    greet_text = "welcome to the MCP server"
    text_content = "Congratz on your first sms message!"

    asyncio.run(main(greet_text, text_content))
