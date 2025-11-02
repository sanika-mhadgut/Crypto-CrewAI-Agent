import os
import requests

class SerperDevTool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")

    def run(self, query: str):
        """
        Queries the Serper.dev API for web search results.
        Returns JSON results with titles, links, and snippets.
        """
        if not self.api_key:
            raise ValueError("Missing SERPER_API_KEY environment variable.")

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": 8}

        try:
            res = requests.post(url, headers=headers, json=payload)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print("Error calling Serper API:", e)
            return {"error": str(e)}
