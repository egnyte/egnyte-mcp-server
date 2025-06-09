from typing import Optional
from mcp.server.fastmcp import FastMCP
from egnyte import EgnyteClient


def register_links(mcp: FastMCP, client: EgnyteClient):
    @mcp.tool()
    async def create_sharing_link_for_object(
        path: str,
        type: str,
        accessibility: str,
        recipients: Optional[list[str]],
        send_email: Optional[bool],
        message: Optional[str],
        copy_me: Optional[bool],
        notify: Optional[bool],
        link_to_current: Optional[bool],
        expiry_date: Optional[str],
        expiry_clicks: Optional[int],
        add_filename: Optional[bool],
    ) -> dict:
        """Creates a sharing link for a file or folder in Egnyte with configurable access and notification settings.

        This function implements the Egnyte Links API to create shareable links for files or folders.
        The link can be configured with various access controls and notification preferences.

        Args:
            path (str): The absolute path of the target file or folder in Egnyte
            type (str): Type of link - must be either "file" or "folder"
            accessibility (str): Who can access the link. Must be one of:
                - "anyone": Anyone with the link can access
                - "password": Password-protected access
                - "domain": Only users in the Egnyte domain can access
                - "recipients": Only specified recipients can access
            recipients (Optional[list[str]]): List of email addresses for recipients. Required if accessibility is "recipients"
            send_email (Optional[bool]): If True, sends the link via email to recipients
            message (Optional[str]): Personal message to include in the email. Supports plain text and basic HTML (<br>, <p>)
            copy_me (Optional[bool]): If True, sends a copy of the link message to the creator
            notify (Optional[bool]): If True, notifies the creator when the link is accessed
            link_to_current (Optional[bool]): If True, link always points to current version of file (file links only)
            expiry_date (Optional[str]): Link expiration date in YYYY-MM-DD format
            expiry_clicks (Optional[int]): Number of clicks before link expires (1-10)
            add_filename (Optional[bool]): If True, appends filename to the link URL (file links only)

        Returns:
            dict: A dictionary containing the created link information, including:
                - id: The unique identifier of the created link
                - url: The full URL of the created link
                - recipients: List of email addresses to which the link was sent (if send_email was True)
                - path: The absolute path of the target resource (file or folder)
                - type: The type of link created (file/folder)
                - accessibility: The access level set for the link (anyone/password/domain/recipients)
                - notify: Whether creator will be notified on access
                - link_to_current: Whether link points to current version (file links only)
                - expiry_date: Expiration date if set (YYYY-MM-DD format)
                - creation_date: When the link was created
                - created_by: Username of the creator
                - protection: Link protection level (PREVIEW or NONE)
                - resource_id: ID of the associated resource
                - expiry_clicks: Number of clicks before expiration (if set)
                - last_accessed: Last access timestamp (if accessed)
                - password: The password for accessing the link (only present when accessibility is "password")

        Note:
            - expiry_date and expiry_clicks are mutually exclusive
            - For password-protected links, a password will be auto-generated if not specified
            - The link will be created with domain-level default settings if useDefaultSettings is True
            - If send_email is True, recipients must be provided
            - The response includes all metadata and configuration settings of the created link
        """
        link = client.links.create(
            path,
            type,
            accessibility,
            recipients,
            send_email,
            message,
            copy_me,
            notify,
            link_to_current,
            expiry_date,
            expiry_clicks,
            add_filename,
        )
        return link

    @mcp.tool()
    async def list_all_links(
        path: Optional[str] = None,
        username: Optional[str] = None,
        created_before: Optional[str] = None,
        created_after: Optional[str] = None,
        type: Optional[str] = None,
        accessibility: Optional[str] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> list:
        """Lists all links in the Egnyte domain with optional filtering parameters.

        This function implements the Egnyte Links API v2 to list all links that the current user has access to.
        If the user is not an admin, only links created by the user will be listed.

        Args:
            path (Optional[str]): Filter links to a specific file or folder by its full path
            username (Optional[str]): Filter links created by a specific user
            created_before (Optional[str]): Filter links created before a given date (ISO-8601 format, e.g., 2022-03-05T14:55:59+0000, which gets converted to 2022-03-05T14:55:59%2B0000)
            created_after (Optional[str]): Filter links created after a given date (ISO-8601 format, e.g., 2022-03-05T14:55:59+0000, which gets converted to 2022-03-05T14:55:59%2B0000)
            type (Optional[str]): Filter by link type - must be either "file" or "folder"
            accessibility (Optional[str]): Filter by accessibility level - must be one of:
                - "anyone": Anyone with the link can access
                - "password": Password-protected access
                - "domain": Only users in the Egnyte domain can access
                - "recipients": Only specified recipients can access
            offset (Optional[int]): The 0-based index of the initial record to return
            count (Optional[int]): Maximum number of entries to return per page (default: 500)

        Returns:
            list: A list of link objects containing detailed information about each link, including:
                - path: The absolute path of the target resource
                - type: The type of link (file/folder)
                - accessibility: Who can access the link
                - protection: Link protection level (PREVIEW or NONE)
                - recipients: List of recipient email addresses
                - notify: Whether creator is notified on access
                - url: The full URL of the link
                - id: The unique identifier of the link
                - link_to_current: Whether link points to current version
                - creation_date: When the link was created
                - created_by: Username of the creator
                - resource_id: ID of the associated resource
                - expiry_clicks: Remaining clicks before expiration (if applicable)
                - expiry_date: Expiration date (if applicable)
                - last_accessed: Last access timestamp (if accessed)
        """
        links = client.links.list_v2(
            path=path,
            username=username,
            created_before=created_before,
            created_after=created_after,
            type=type,
            accessibility=accessibility,
            offset=offset,
            count=count,
        )
        return links

    @mcp.tool()
    async def get_link_by_id(link_id: str) -> dict:
        """Retrieves detailed information about a specific link in the Egnyte domain.

        This function implements the Egnyte Links API to fetch comprehensive details about a single link
        using its unique identifier. The response includes all metadata and configuration settings
        associated with the link.

        Args:
            link_id (str): The unique identifier of the link to retrieve. This is the ID portion of the link URL
                          (e.g., for URL 'https://domain.egnyte.com/dl/abc123', the link_id would be 'abc123')

        Returns:
            dict: A dictionary containing detailed information about the link, including:
                - path: The absolute path of the target resource (file or folder)
                - type: The type of link (file/folder)
                - accessibility: Who can access the link (anyone/password/domain/recipients)
                - protection: Link protection level (PREVIEW or NONE)
                - recipients: List of recipient email addresses
                - notify: Whether creator is notified on access
                - url: The full URL of the link
                - id: The unique identifier of the link
                - link_to_current: Whether link points to current version
                - creation_date: When the link was created
                - created_by: Username of the creator
                - resource_id: ID of the associated resource
                - expiry_clicks: Remaining clicks before expiration (if applicable)
                - expiry_date: Expiration date (if applicable)
                - last_accessed: Last access timestamp (if accessed)

        Note:
            - The link must exist and the user must have permission to view it
            - If the link has been deleted or expired, this will return an error
            - Non-admin users can only view links they created
        """
        link = client.links.get(link_id)
        return link

    @mcp.tool()
    async def delete_link_by_id(link_id: str) -> dict:
        """Deletes a specific link from the Egnyte domain.

        This function implements the Egnyte Links API to permanently delete a link using its unique identifier.
        Once deleted, the link cannot be recovered and any existing access to the link will be revoked.

        Args:
            link_id (str): The unique identifier of the link to delete. This is the ID portion of the link URL
                          (e.g., for URL 'https://domain.egnyte.com/dl/abc123', the link_id would be 'abc123')

        Returns:
            dict: A dictionary containing the result of the deletion operation, typically including:
                - success: Boolean indicating if the deletion was successful
                - message: Description of the operation result

        Note:
            - The link must exist and the user must have permission to delete it
            - Non-admin users can only delete links they created
            - This operation is permanent and cannot be undone
            - Any users with the link will no longer be able to access the resource through this link
        """
        result = client.links.get(link_id)
        if result.check:
            result = result.delete()

        return result
