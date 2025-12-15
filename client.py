import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define the server we want to talk to.
# We use 'sys.executable' to make sure we use the SAME Python environment
# that is currently running this script.
server_params = StdioServerParameters(
    command=sys.executable, 
    args=["server.py"], 
    env=None
)

async def run_client():
    print("🤖 Connecting to server...")
    
    # Start the server process and connect to its stdin/stdout
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Step 1: Initialize
            await session.initialize()
            
            # Step 2: List Available Tools
            tools = await session.list_tools()
            print(f"\n✅ Connected! Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"   - {tool.name}: {tool.description}")

            # Step 3: Call the 'list_files' tool
            print("\n📂 Executing 'list_files'...")
            result = await session.call_tool("list_files", arguments={})
            
            # Display the result
            print("--- SERVER RESPONSE ---")
            print(result.content[0].text)
            print("-----------------------")

            # Step 4: Call the 'read_file' tool (let's try reading hello.txt)
            # Make sure 'hello.txt' actually exists in your test_notes folder!
            print("\n📖 Executing 'read_file' for 'hello.txt'...")
            read_result = await session.call_tool("read_file", arguments={"filename": "hello.txt"})
            
            print("--- FILE CONTENT ---")
            print(read_result.content[0].text)
            print("--------------------")

if __name__ == "__main__":
    asyncio.run(run_client())