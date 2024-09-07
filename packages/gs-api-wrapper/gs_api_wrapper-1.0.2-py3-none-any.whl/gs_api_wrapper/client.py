# src/client.py
import base64
import requests


class GoldenSourceClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth_header = self._create_auth_header(username, password)

    def _create_auth_header(self, username, password):
        """Encode username and password for Basic Auth."""
        credentials = f"{username}:{password}"
        token = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }

    def get(self, endpoint, params=None):
        """Generic GET request."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.auth_header, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data):
        """Generic POST request."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.auth_header, json=data)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle API responses."""
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
