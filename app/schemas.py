from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# =================================================================
# 1. INCOMING WEBHOOK SCHEMAS
#    These models validate the raw data received from external chat platforms.
# =================================================================


class TelegramUser(BaseModel):
    """Represents the user who sent the message."""
    id: str

class TelegramChat(BaseModel):
    """Represents the chat where the message was sent."""
    id: str

class TelegramMessage(BaseModel):
    """Represents a message from Telegram."""
    message_id: int
    chat: TelegramChat
    from_user: TelegramUser = Field(..., alias='from') # 'from' is a reserved keyword
    text: Optional[str] = None # Text is optional as it could be a photo, sticker, etc.

class TelegramWebhookPayload(BaseModel):
    """The top-level object sent by Telegram to our webhook."""
    update_id: int
    message: TelegramMessage


# --- Soroush Schemas ---

class SoroushCallbackData(BaseModel):
    """Represents the data from a button press in Soroush."""
    data: str

class SoroushUpdate(BaseModel):
    """Represents a single message or event from Soroush."""
    from_user: str = Field(..., alias='from')
    text: Optional[str] = None
    callback_data: Optional[SoroushCallbackData] = None

class SoroushWebhookPayload(BaseModel):
    """The top-level object Soroush sends, containing a list of updates."""
    data: List[SoroushUpdate]


# =================================================================
# 2. UNIVERSAL REQUEST SCHEMA (Gateway -> Core Chatbot)
#    This is the standardized format for all messages sent to your main chatbot API.
# =================================================================

class GatewaySendMessageRequest(BaseModel):
    """
    The universal format that the Gateway uses to send a message
    to the core chatbot service for processing.
    """
    user_id: str
    session_id: str
    query: str
    source_platform: str  # e.g., "telegram", "soroush"
    metadata: Dict[str, Any] = {} # For any extra platform-specific data


# =================================================================
# 3. UNIVERSAL RESPONSE SCHEMA (Core Chatbot -> Gateway)
#    This is the standardized format the Gateway expects back from the chatbot.
# =================================================================

class ChatbotResponseReference(BaseModel):
    """Represents a single source document or reference."""
    name: str
    type: str
    url: str
    chunk_id: int
    content: str
    tags: List[str]
    score: str

class ChatbotResponse(BaseModel):
    """
    The universal format that the Gateway expects to receive from the
    core chatbot service after a message has been processed.
    """
    text: str
    references: List[ChatbotResponseReference] = []
    # We can add more fields here in the future, like buttons or media attachments.

