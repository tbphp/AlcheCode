"""Parse JSON from markdown content."""

import json
import re


def parse_llm_json(content: str) -> dict:
    """Parse JSON from markdown content."""
    # 尝试匹配```json块中的内容
    json_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(json_block_pattern, content)

    if matches:
        # 使用第一个匹配的json块
        return json.loads(matches[0])

    # 使用更可靠的方式来匹配JSON
    def find_json_string(text):
        stack = []
        start = -1

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

    # 尝试查找和解析JSON字符串
    json_str = find_json_string(content)
    if json_str:
        return json.loads(json_str)

    # 如果上述都没匹配到，则尝试直接解析整个内容
    return json.loads(content)
