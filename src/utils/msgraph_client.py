from azure.identity import InteractiveBrowserCredential
from msgraph import GraphServiceClient
from interfaces.msgraph_client_interface import MSGraphClientBase
from typing import Dict, Any
import os

class MSGraphClient(MSGraphClientBase):
    """Real implementation of Microsoft Graph client operations"""
    
    def __init__(self):
        """Initialize the Graph client with Azure credentials"""
        credentials = InteractiveBrowserCredential(
            client_id=os.getenv("AZURE_CLIENT_ID"),
            tenant_id=os.getenv("AZURE_TENANT_ID")
        )
        scopes = ['https://graph.microsoft.com/.default']
        self.graph_client = GraphServiceClient(credentials=credentials, scopes=scopes)

    async def get_sharepoint_site_pages(self, site_id: str) -> Dict[str, Any]:
        """Get all pages for a SharePoint site
        
        Args:
            site_id: The ID of the SharePoint site
            
        Returns:
            Dict containing the pages data
        """
        result = await self.graph_client.sites.by_site_id(site_id).pages.get()
        if not result:
            print(f"No result found for site with id: {site_id}")
        return result

    async def get_sharepoint_site_page_webparts(self, site_id: str, page_id: str) -> Dict[str, Any]:
        """Get all webparts for a specific SharePoint page
        
        Args:
            site_id: The ID of the SharePoint site
            page_id: The ID of the page
            
        Returns:
            Dict containing the webparts data
        """
        result = await self.graph_client.sites.by_site_id(site_id).pages.by_base_site_page_id(page_id).graph_site_page.web_parts.get()
        if not result:
            print(f"No results found for site: {site_id} and page: {page_id}")
        return result
