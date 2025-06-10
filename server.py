from typing import Any
import httpx
from fastmcp import FastMCP
from requests.auth import HTTPBasicAuth
from typing import List, Optional
from egnyte import configuration, client
from modules import register_links


# from import domain, access_token

# Initialize FastMCP server
mcp = FastMCP("Egnyte MCP Server")

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access the variables
domain = os.getenv("DOMAIN")
access_token = os.getenv("ACCESS_TOKEN")


client = client.EgnyteClient({"domain": domain, "access_token": access_token})
register_links(mcp, client)


@mcp.tool()
async def search_for_document_by_name(file_name: str) -> str:
    """Searche an Egnyte domain for a document by name and returns the document text snippet"""
    search_results = client.search.files(file_name)
    return search_results[0].snippet


if __name__ == "__main__":
    mcp.run()
