import httpx
from app.schemas import TelegramWebhookPayload, GatewaySendMessageRequest, ChatbotResponse
from app.services.chatbot_client import chatbot_client
from app.config import settings

async def process_telegram_update(payload: TelegramWebhookPayload):
    """
    Processes a validated webhook payload from Telegram.
    
    1. Transforms the Telegram message into a universal format.
    2. Sends the universal message to the core chatbot API.
    3. Receives the response from the chatbot.
    4. Sends the final reply back to the user on Telegram.
    """
    message = payload.message
    
    # We only process text messages for now.
    if not message.text:
        print(f"Ignoring non-text message from user {message.from_user.id}")
        return

    # 1. Transform into our universal format
    universal_request = GatewaySendMessageRequest(
        user_id=str(message.from_user.id),
        session_id=str(message.chat.id),
        query=message.text,
        source_platform="telegram",
        metadata={"telegram_message_id": message.message_id}
    )

    try:
        chatbot_response = await chatbot_client.send_message(universal_request)
    except Exception as e:
        # If the core chatbot is down or returns an error,
        # we need to inform the user and stop.
        print(f"An error occurred while communicating with the core chatbot: {e}")
        await send_reply_to_telegram(
            chat_id=message.chat.id,
            text="Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."
        )
        return

    await send_reply_to_telegram(
        chat_id=message.chat.id,
        text=chatbot_response.text
    )


async def send_reply_to_telegram(chat_id: str, text: str):
    """
    Sends a text message back to a user on Telegram.
    """
    telegram_api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(telegram_api_url, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            print(f"Successfully sent reply to Telegram chat ID {chat_id}")
        except httpx.HTTPStatusError as e:
            print(f"Error sending reply to Telegram: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Network error sending reply to Telegram: {e}")

