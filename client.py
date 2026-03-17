import asyncio
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp import StdioServerParameters
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

server_params = StdioServerParameters(
    command="uv",
    args=["run","mcp_server.py"],
    env=None,
)

async def main():

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            tools_response = await session.list_tools()
            print("Available tools:", [t.name for t in tools_response.tools])

            if "get_docs" in [t.name for t in tools_response.tools]:
                print("\nTesting 'get_docs' tool...")
                result = await session.call_tool("get_docs", arguments={"query": "how to install", "library": "uv"})
                print("\nTool result:")
                print(result.content[0].text if result.content else "No content returned")

if __name__ == "__main__":
    asyncio.run(main())
            

