from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport
import asyncio

server_script = "server.py" # Assumes this file exists and runs mcp.run()

transport = PythonStdioTransport(
    script_path="mcp/server/server.py"   
)

client = Client(transport)

async def use_stdio_client(client):
    async with client:
        tools = await client.list_tools()
        print(f"Connected via Python Stdio, found tools: {tools}")

        query = "expense_tracker_requirements.txt"
        # Wrap the query in a dictionary with the expected key
        arguments = {"file_name": query}
        # Call the tool with the correct arguments format
        response = await client.call_tool("search_for_document_by_name", arguments)

        print(f"Answer: {response}")
        
asyncio.run(use_stdio_client(client))