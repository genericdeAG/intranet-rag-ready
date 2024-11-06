from abc import ABC, abstractmethod
from typing import Dict, Any

class MSGraphClientBase(ABC):
    """Abstract base class for Microsoft Graph client operations"""
    
    @abstractmethod
    async def get_sharepoint_site_pages(self, site_id: str) -> Dict[str, Any]:
        """Get all pages for a SharePoint site
        
        Args:
            site_id: The ID of the SharePoint site
            
        Returns:
            Dict containing the pages data
        """
        pass
    
    @abstractmethod
    async def get_sharepoint_site_page_webparts(self, site_id: str, page_id: str) -> Dict[str, Any]:
        """Get all webparts for a specific SharePoint page
        
        Args:
            site_id: The ID of the SharePoint site
            page_id: The ID of the page
            
        Returns:
            Dict containing the webparts data
        """
        pass
