"""
Package for CR (Clash Royale) API."""

import requests


class ClashRoyaleAPI:
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.clashroyale.com/v1/"
        self.headers = {}

    def set_api_key(self, api_key: str):
        """Set the API key and update headers."""
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

    def get_player_info(self, player_tag: str):
        """Get information about a specific player."""
        if not self.api_key:
            raise ValueError("API key must be set before making requests.")
        url = f"{self.base_url}players/%23{player_tag[1:]}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


# Create an instance of ClashRoyaleAPI that can be accessed globally
api = ClashRoyaleAPI()
