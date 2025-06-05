import os

from dotenv import load_dotenv
from egnyte import client
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Egnyte Document Store Retriever")

# Load .env file
load_dotenv()

# Access the variables
domain = os.getenv('DOMAIN')
access_token = os.getenv('ACCESS_TOKEN')

client = client.EgnyteClient({"domain": domain, "access_token": access_token})


@mcp.tool()
async def search_for_document_by_name(file_name: str) -> str:
    """Search an Egnyte domain for a document by name and returns the document text snippet"""
    search_results = client.search.files(file_name)
    return search_results[0].snippet


if __name__ == "__main__":
    mcp.run()
