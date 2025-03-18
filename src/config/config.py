"""Config module."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class Config:
    """Config."""

    app_name: str = os.getenv("APP_NAME", "AlcheCode")
    """应用名称"""

    api_host: str = os.getenv("API_HOST", "127.0.0.1")
    """API服务主机地址"""

    api_port: int = int(os.getenv("API_PORT", 3300))
    """API服务端口"""

    model: str = os.getenv("MODEL_NAME", "openai:gpt-3.5-turbo")
    """LLM模型名称，需要以[供应商:模型名称]的格式，例如openai:gpt-3.5-turbo"""

    max_input_size = 1 * 1024 * 1024
    """最大输入大小，单位字节"""

    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    """意图识别的置信度阈值，范围0到1"""

    llm_language: str = os.getenv("LLM_LANGUAGE", "English")
    """LLM返回的提示语的语言"""
