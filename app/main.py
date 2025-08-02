from fastapi import FastAPI
from app.api import webhooks

# Create the main FastAPI application instance
app = FastAPI(
    title="Chatbot Gateway",
    description="An independent service to handle webhooks from various chat platforms and route them to the core chatbot API.",
    version="1.0.0"
)

# Include the router from the webhooks module.
# This makes all the endpoints defined in webhooks.py available under the main app.
# We can add a prefix if we want all webhook URLs to start with something specific,
# e.g., app.include_router(webhooks.router, prefix="/gateway")
app.include_router(webhooks.router)

@app.get("/", tags=["Default"])
def read_root():
    """A simple endpoint to confirm the gateway is running."""
    return {"message": "Chatbot Gateway is running"}

