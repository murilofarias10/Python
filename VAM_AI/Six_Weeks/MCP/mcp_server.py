"""
This is a MCP server that can be used to send text messages to phone numbers via Surge API.
"""

import httpx
import json

from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP(name="My MCP Server")

"""
Load surge config
Do these steps:
    1. Create a surge_config.json file in the private folder
    2. Sign up for a Surge account at https://surgemsg.com/
    3. Add the following content to the surge_config.json file:
    {
        "api_key": "find in SURGE account settings",
        "account_id": "find in SURGE account settings",
        "my_phone_number": "your phone number",
        "my_first_name": "your first name",
        "my_last_name": "your last name"
    }
    Save the file in the private folder
"""
with open("private/surge_config.json", "r") as f:
    surge_config = json.load(f)


@mcp.tool
def greet(text_content: str) -> str:
    """Returns a friendly greeting."""
    return text_content


@mcp.tool(name="textme", description="Send a text message to me")
def send_text_message(text_content: str) -> str:
    """Internal function to send a text message via Surge API"""

    # Set up Surge API client and send text message
    with httpx.Client() as client:
        response = client.post(
            "https://api.surgemsg.com/messages",
            headers={
                "Authorization": f"Bearer {surge_config['api_key']}",
                "Surge-Account": surge_config["account_id"],
                "Content-Type": "application/json",
            },
            json={
                "body": text_content,
                "conversation": {
                    "contact": {
                        "first_name": surge_config["my_first_name"],
                        "last_name": surge_config["my_last_name"],
                        "phone_number": surge_config["my_phone_number"],
                    }
                },
            },
        )
        response.raise_for_status()
        return f"Message sent: {text_content}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path="/mcp")
