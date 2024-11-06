import json
import os
from typing import Dict, Any
from interfaces.msgraph_client_interface import MSGraphClientBase

class MockMSGraphClient(MSGraphClientBase):
    """Mock implementation of Microsoft Graph client operations using local JSON files"""
    
    def __init__(self, data_dir: str = "data/ms-graph"):
        """Initialize the mock client with the data directory path
        
        Args:
            data_dir: Path to directory containing mock JSON data files
        """
        self.data_dir = data_dir

    async def get_sharepoint_site_pages(self, site_id: str) -> Dict[str, Any]:
        """Get all pages for a SharePoint site from mock data
        
        Args:
            site_id: The ID of the SharePoint site
            
        Returns:
            Dict containing the pages data from local JSON file
        """
        # Construct the file path for the site pages data
        file_path = os.path.join(self.data_dir, "list-all-pages", f"{site_id}.json")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"No mock data found for site pages with id: {site_id}")
            return {"value": []}

    async def get_sharepoint_site_page_webparts(self, site_id: str, page_id: str) -> Dict[str, Any]:
        """Get all webparts for a specific SharePoint page from mock data
        
        Args:
            site_id: The ID of the SharePoint site
            page_id: The ID of the page
            
        Returns:
            Dict containing the webparts data from local JSON file
        """
        # Construct the file path for the page webparts data
        file_path = os.path.join(self.data_dir, "list-all-webparts", site_id, f"{page_id}.json")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"No mock data found for webparts with site: {site_id} and page: {page_id}")
            return {"value": []}
