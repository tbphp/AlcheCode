"""Config module."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class Config:
    """Config."""

    app_name: str = os.getenv("APP_NAME", "AlcheCode")

    api_host: str = os.getenv("API_HOST", "127.0.0.1")

    api_port: int = int(os.getenv("API_PORT", 3300))

    model: str = os.getenv("MODEL_NAME", "openai:gpt-3.5-turbo")

    max_input_size = 1 * 1024 * 1024  # 1MB

    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))

    llm_language: str = os.getenv("LLM_LANGUAGE", "English")
