import os
import httpx
import json
from typing import Dict, List, Union, Any, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class SearchQuery(BaseModel):
    """Input model for Brave Search queries."""
    query: str = Field(..., description="The search query string")
    count: int = Field(10, description="Number of results to return (1-20)")
    offset: int = Field(0, description="Pagination offset (max 9, default 0)")

class BraveSearchTool:
    """
    Tool that performs searches using the Brave Search API.
    Requires a BRAVE_API_KEY environment variable.
    """
    def __init__(self, api_key: str = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY is required")
        self.timeout = timeout
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }

    async def async_search(self, query: str, count: int = 10, offset: int = 0) -> List[Dict[str, str]]:
        """
        Perform an asynchronous search using the Brave Search API.
        
        Args:
            query: The search query
            count: Number of results to return (1-20)
            offset: Pagination offset
            
        Returns:
            List of search results with title, url, and description
        """
        params = {"q": query, "count": count, "offset": offset}
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return self._format_results(data)
        except Exception as e:
            return [{"error": f"Async search failed: {str(e)}"}]

    def search(self, query: str, count: int = 10, offset: int = 0) -> List[Dict[str, str]]:
        """
        Perform a synchronous search using the Brave Search API.
        
        Args:
            query: The search query
            count: Number of results to return (1-20)
            offset: Pagination offset
            
        Returns:
            List of search results with title, url, and description
        """
        params = {"q": query, "count": count, "offset": offset}
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    self.base_url,
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()
                return self._format_results(data)
        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]

    def _format_results(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Format the raw API response into a clean list of results.
        
        Args:
            data: Raw API response data
            
        Returns:
            List of formatted search results
        """
        results = []
        if "web" not in data or "results" not in data["web"]:
            return [{"error": "No results found in API response"}]
            
        for item in data["web"]["results"]:
            results.append({
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "description": item.get("description", "No description available")
            })
        return results

# Note: CrewAI tool definitions are removed as they might vary between versions
# If you need to create CrewAI tools, check the current CrewAI documentation
# and implement them accordingly