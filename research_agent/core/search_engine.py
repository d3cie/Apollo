from typing import List
from serpapi import GoogleSearch
import aiohttp


class SearchEngine:
    def __init__(self, serp_api_key: str):
        self.api_key = serp_api_key

    async def search(self, query: str, num_results: int = 5) -> List[dict]:
        """
        Perform a Google search using SerpAPI and return formatted results.

        Args:
            query: The search query string
            num_results: Maximum number of results to return (default: 5)

        Returns:
            List of dictionaries containing search results with title, link, and snippet
        """
        search = GoogleSearch(
            {
                "q": query,
                "api_key": self.api_key,
                "num": num_results,
                "engine": "google",
                "filter": 1,
                "safe": "active",
            }
        )

        results = search.get_dict()
        organic_results = results.get("organic_results", [])

        formatted_results = []
        for result in organic_results:
            formatted_results.append(
                {
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                }
            )

        return formatted_results[:num_results]

    async def validate_url(self, url: str) -> bool:
        """
        Validate if a URL is accessible.

        Args:
            url: The URL to validate

        Returns:
            bool: True if URL is accessible, False otherwise
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True) as response:
                    return response.status == 200
        except:
            return False
