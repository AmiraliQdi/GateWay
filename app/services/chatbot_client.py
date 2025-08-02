# app/services/chatbot_client.py

import httpx
from app.schemas import GatewaySendMessageRequest, ChatbotResponse
from app.config import settings

class ChatbotClient:
    """
    A client for communicating with the core chatbot service.
    Handles sending messages and parsing responses.
    """
    def __init__(self):
        # The base URL for the core chatbot API is loaded from our settings.
        self.api_url = settings.CHATBOT_API_URL
        if not self.api_url:
            raise ValueError("CHATBOT_API_URL is not set in the environment.")

    async def send_message(self, request_data: GatewaySendMessageRequest) -> ChatbotResponse:
        """
        Sends a standardized message request to the core chatbot API.

        Args:
            request_data: The message payload in the universal format.

        Returns:
            A ChatbotResponse object with the AI's reply.
            
        Raises:
            Exception: If the API call fails or returns an error.
        """
        # We use an async client for non-blocking network calls.
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                print(f"Forwarding request to core chatbot at: {self.api_url}")
                
                # Make the POST request, sending the Pydantic model as JSON
                response = await client.post(
                    self.api_url,
                    json=request_data.model_dump()
                )

                # Raise an exception for bad status codes (4xx or 5xx)
                response.raise_for_status()

                # Parse the successful response into our universal response schema
                chatbot_response = ChatbotResponse(**response.json())
                
                return chatbot_response

            except httpx.HTTPStatusError as e:
                # Log the specific error from the backend
                print(f"Error from chatbot API: {e.response.status_code} - {e.response.text}")
                raise Exception("The core chatbot service returned an error.") from e
            
            except httpx.RequestError as e:
                # Log network-level errors
                print(f"Could not connect to chatbot API at {self.api_url}: {e}")
                raise Exception("Failed to connect to the core chatbot service.") from e

# Create a single, reusable instance of the client for our application to use.
chatbot_client = ChatbotClient()

