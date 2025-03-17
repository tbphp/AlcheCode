"""Config module."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class Config:
    """Config."""

    model: str = os.getenv("MODEL_NAME", "openai:gpt-3.5-turbo")

    max_input_size = 1 * 1024 * 1024  # 1MB

    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))

    llm_language: str = os.getenv("LLM_LANGUAGE", "English")
