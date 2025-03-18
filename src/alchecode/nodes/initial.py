import re

from config import Config, State


def normalize_input(input_str: str) -> str:
    """将输入字符串规范化为LF并删除多余的换行符"""
    normalized = input_str.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"\n+", "\n", normalized)
    return normalized.strip()


def detect_injection(input_str: str) -> bool:
    """检测潜在的注入攻击"""
    patterns = [r"\$\{.*\}", r"<\?.*\?>", r"`.*`"]
    return any(re.search(p, input_str) for p in patterns)


def initial_node(state: State) -> None:
    """初始节点，用于输入验证和预处理"""
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
