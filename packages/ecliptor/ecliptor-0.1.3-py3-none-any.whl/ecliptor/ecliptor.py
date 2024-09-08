import requests
from typing import List, Dict, Any
from .exceptions import EcliptorAPIError

class Ecliptor:
    def __init__(self, api_key: str, base_url: str = "https://api.ecliptor.ai"):
        """
        Initialize the Ecliptor client.

        Args:
            api_key (str): The API key for authentication.
            base_url (str, optional): The base URL for the Ecliptor API. Defaults to "https://api.ecliptor.com".
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",  # API key passed in the header
            "Content-Type": "application/json"
        })

    def adapt(self, embedding: List[float], adapter_name: str, embedding_size: int) -> Dict[str, Any]:
        """
        Process a vector embedding by sending it to the Ecliptor API.

        Args:
            embedding (List[float]): The input vector embedding.
            adapter_name: unique identifier for the adapter
            embedding_size (int): The size of the embedding vector.

        Returns:
            Dict[str, Any]: The processed results from the API.

        Raises:
            EcliptorAPIError: If the API request fails.
        """
        data = {
            "api_key": self.api_key,
            "embedding": embedding,
            "adapter_name": adapter_name,
            "embedding_size": embedding_size
        }

        try:
            response = self.session.post(f"{self.base_url}/v1/adapt", json=data)
            response.raise_for_status()
            return response.json()[0]["finetuned_embedding"] # Just return the list of floats
        except requests.exceptions.RequestException as e:
            raise EcliptorAPIError(f"API request failed: {str(e)}") from e

    def close(self):
        """
        Close the session.
        """
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()