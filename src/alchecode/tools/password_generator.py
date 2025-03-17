"""Password generator tool."""

import random
import re
import string
from typing import Any

from . import tool
from .base import BaseTool


@tool
class PasswordGeneratorTool(BaseTool):
    """Password generator tool."""

    name = "password_generator"
    description = "生成随机密码"
    input_schema = {
        "type": "object",
        "properties": {
            "length": {
                "type": "integer",
                "description": "密码长度",
                "minimum": 6,
                "maximum": 64,
                "default": 12,
            },
            "use_symbols": {
                "type": "boolean",
                "description": "是否包含特殊符号",
                "default": True,
            },
            "use_numbers": {
                "type": "boolean",
                "description": "是否包含数字",
                "default": True,
            },
            "use_uppercase": {
                "type": "boolean",
                "description": "是否包含大写字母",
                "default": True,
            },
        },
        "required": [],
    }
    patterns = [
        re.compile(r"^(pwd|password|pass|密码)(\s*(\d+))?$", re.IGNORECASE),
        re.compile(r"^(\d+)\s*(pwd|password|pass|密码)$", re.IGNORECASE),
    ]
    param_validators = {
        "length": lambda x: isinstance(x, int) and 6 <= x <= 64,
        "use_symbols": lambda x: isinstance(x, bool),
        "use_numbers": lambda x: isinstance(x, bool),
        "use_uppercase": lambda x: isinstance(x, bool),
    }

    def extract_params(self, index: int, match: re.Match[str]) -> dict[str, Any]:
        """Extract parameters."""
        params = {}
        group_num = 3 if index == 0 else 1
        group_value = match.group(group_num)
        if group_value:
            params["length"] = int(group_value)
        return params

    def execute(self, params: dict[str, Any]) -> str:
        """Execute."""
        length = params.get(
            "length", self.input_schema["properties"]["length"]["default"]
        )
        use_symbols = params.get(
            "use_symbols", self.input_schema["properties"]["use_symbols"]["default"]
        )
        use_numbers = params.get(
            "use_numbers", self.input_schema["properties"]["use_numbers"]["default"]
        )
        use_uppercase = params.get(
            "use_uppercase", self.input_schema["properties"]["use_uppercase"]["default"]
        )

        chars = string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += string.punctuation

        return "".join(random.choice(chars) for _ in range(length))
