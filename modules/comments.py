from typing import Optional, List

from egnyte.resources import Note
from mcp.server.fastmcp import FastMCP
from egnyte import EgnyteClient


def register_comments(mcp: FastMCP, client: EgnyteClient):

    @mcp.tool()
    async def create_comment_on_file(
        path: str,
        text: str
    ) -> Note:
        """
            Create a new comment on a file in Egnyte.
            Parameters:

            * path - path to the file the comment is about
            * message - contents of the comment

            Returns the created comment as a Note object.
        """
        comment = client.notes.create(path, text)
        return comment

    @mcp.tool()
    async def list_comments(
        file_path: Optional[str] = None,
        folder_path: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Note]:
        """
            List existing notes.
            Optional filtering parameters:

            * start_time: Get notes created after start_time (datetime.date or string in 'YYYY-MM-DD' format)
            * file: Get only notes attached to a specific file (path).
            * folder: Get only notes attached to files in specific folder (path).
            * end_time: Get notes created before end_time (datetime.date or string in 'YYYY-MM-DD' format)

            Returns list comments as a Note objects, with additional attributes total_count and offset.
        """
        comments = client.notes.list(file_path, folder_path, start_time, end_time)
        return comments
