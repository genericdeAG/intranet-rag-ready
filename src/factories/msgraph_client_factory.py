from typing import Optional
from interfaces.msgraph_client_interface import MSGraphClientBase
from utils.msgraph_client import MSGraphClient
from utils.mock_msgraph_client import MockMSGraphClient

class MSGraphClientFactory:
    """Factory class for creating MS Graph clients"""
    
    _instance: Optional[MSGraphClientBase] = None
    
    @classmethod
    def get_client(cls, use_mock: bool = False) -> MSGraphClientBase:
        """Get a singleton instance of the MS Graph client
        
        Args:
            use_mock: If True, returns a mock client, otherwise returns real client
            
        Returns:
            An instance of MSGraphClientBase
        """
        if cls._instance is None:
            if use_mock:
                cls._instance = MockMSGraphClient()
            else:
                cls._instance = MSGraphClient()
        return cls._instance
    
    @classmethod
    def reset_client(cls) -> None:
        """Reset the singleton instance"""
        cls._instance = None
