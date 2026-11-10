import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv(Path(__file__).resolve().parent / ".env")

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0, reasoning_format="parsed")

stdio_server_params = StdioServerParameters(
    command=sys.executable,
    args=[str(Path(__file__).resolve().parent / "servers" / "math_server.py")],
)


async def main():
    print("Hello from mcp-crash-course!")
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)

            agent = create_agent(llm, tools)

            result = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 54 + 2 * 3?")]}
            )
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
