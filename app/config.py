import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages all application settings and environment variables.
    Pydantic's BaseSettings will automatically read variables from the
    environment or a .env file.
    """
    # --- Core Chatbot API ---
    # The full URL to the core chatbot's send_message endpoint.
    CHATBOT_API_URL: str

    # --- Telegram Configuration ---
    # The secret token for the Telegram bot that this gateway will manage.
    TELEGRAM_BOT_TOKEN: str

    # This tells Pydantic to look for a .env file if the variables
    # are not set in the environment.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

# Create a single, globally accessible instance of the settings.
# Other modules in our application will import this 'settings' object.
settings = Settings()

