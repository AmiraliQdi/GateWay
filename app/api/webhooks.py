# app/api/webhooks.py

from fastapi import APIRouter, Request, HTTPException, status
from app.schemas import TelegramWebhookPayload
from app.adapters import telegram_adapter

# Create a new APIRouter. This helps organize our endpoints.
# All endpoints defined here will be included in the main FastAPI app.
router = APIRouter(
    prefix="/webhook", # All routes in this file will start with /webhook
    tags=["Webhooks"], # Group these endpoints under "Webhooks" in the API docs
)

@router.post("/telegram")
async def handle_telegram_webhook(payload: TelegramWebhookPayload, request: Request):
    """
    This endpoint receives webhook updates from Telegram.
    It validates the incoming data against the TelegramWebhookPayload schema
    and passes it to the Telegram adapter for processing.
    """
    try:
        # The main logic is handled by the adapter. This keeps our API layer clean.
        await telegram_adapter.process_telegram_update(payload)
        
        # Telegram doesn't require a specific response body, just a 200 OK status
        # to acknowledge that we have received the update.
        return {"status": "ok"}

    except Exception as e:
        # This is a general catch-all for any unexpected errors during processing.
        print(f"Error processing Telegram webhook: {e}")
        # It's good practice to still return a 200 OK to Telegram to prevent
        # it from resending the same update, while logging the error internally.
        # However, for debugging, we can return an error.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred: {e}"
        )

# You can add more webhook endpoints here in the future, for example:
# @router.post("/soroush")
# async def handle_soroush_webhook(payload: SoroushWebhookPayload):
#     ...
