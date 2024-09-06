import os
from typing import Optional, Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

class GoLean:
    """Client for interacting with the GoLean API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GoLean client.

        Args:
            api_key (str, optional): The API key for authentication. If not provided,
                                     it will be read from the GOLEAN_API_KEY environment variable.

        Raises:
            ValueError: If the API key is not provided and not found in environment variables.
        """
        self.api_key = api_key or os.getenv("GOLEAN_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it as GOLEAN_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://prompt-compression-api.golean.ai"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def compress_prompt(self, context: str, question: str, compression_rate: float = 0.5, model: str = "gpt-4o") -> Dict[str, Any]:
        """
        Compress a prompt using the GoLean API.

        Args:
            context (str): The context for the prompt.
            question (str): The question to be compressed.
            compression_rate (float, optional): The desired compression rate. Defaults to 0.5.
            model (str, optional): The model to use for compression. Defaults to "gpt-4o".

        Returns:
            Dict[str, Any]: The API response containing the compressed prompt and related metadata.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/compress_prompt/"
        payload = {
            "context": context,
            "question": question,
            "compression_rate": compression_rate,
            "model": model
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()