"""Initialize the LangGraph Agent node."""

import re

from config import Config, State


def normalize_input(input_str: str) -> str:
    """Normalize the input string to LF and remove extra newlines."""
    normalized = input_str.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"\n+", "\n", normalized)
    return normalized.strip()


def detect_injection(input_str: str) -> bool:
    """Detect potential injection attacks."""
    patterns = [r"\$\{.*\}", r"<\?.*\?>", r"`.*`"]
    return any(re.search(p, input_str) for p in patterns)


def initial_node(state: State) -> None:
    """Process the input and return the updated state."""
    # 输入验证
    if not state.input.strip():
        raise OSError("EMPTY_INPUT")

    if len(state.input) > Config.max_input_size:
        raise OSError("EXCEED_LENGTH_LIMIT")

    # 标准化处理
    state.input = normalize_input(state.input)

    # 安全性检查
    if detect_injection(state.input):
        raise OSError("INVALID_ENCODING")
