from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pydantic import Field, BaseModel
from uuid import UUID
import requests
from ..config import get_settings, ConfigurationError

class APIResult(BaseModel):
    """
    Represents the result of an upload operation to the Glean Indexing API.
    """
    success: bool
    status_code: int
    message: Optional[str] = None
    api_response: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    records_uploaded: Optional[int] = 0
    upload_id: Optional[str] = None
    version: Optional[int] = None
    records_fetched: Optional[int] = 0
    data: Optional[Any] = None

class BaseAPI:
    def __init__(self, domain: str):
        self.base_url = f"https://{domain}"

    def _make_request(self, method: str, endpoint: str, headers: Optional[dict] = None, data: Optional[dict] = None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, data=data)
        
        return APIResult(
            success=response.ok,
            status_code=response.status_code,
            api_response=response.text,
            timestamp=datetime.now()
        )
    
