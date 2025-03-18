import json
import re
from typing import Any


def find_json_string(text: str) -> str | None:
    stack: list[str] = []
    start: int = -1

    for i, char in enumerate(text):
        if char in "{[" and not stack:
            start = i
            stack.append(char)
        elif char in "{[":
            stack.append(char)
        elif char == "}" and stack and stack[-1] == "{":
            stack.pop()
        elif char == "]" and stack and stack[-1] == "[":
            stack.pop()

        if start != -1 and not stack:
            return text[start : i + 1]
    return None


def parse_llm_json(content: str) -> Any:
    """从Markdown解析JSON数据

    Args:
        content (str): 输入的Markdown内容
    Returns:
        Any: 解析后的JSON对象
    """
    # 尝试匹配```json块中的内容
    json_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(json_block_pattern, content)

    if matches:
        # 使用第一个匹配的json块
        return json.loads(matches[0])

    # 尝试查找和解析JSON字符串
    json_str = find_json_string(content)
    if json_str:
        return json.loads(json_str)

    # 如果上述都没匹配到，则尝试直接解析整个内容
    return json.loads(content)
