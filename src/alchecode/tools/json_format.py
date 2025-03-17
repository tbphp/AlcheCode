"""Json Format Tool."""

import json
import re
from typing import Any

from . import tool
from .base import BaseTool


@tool
class JsonFormatTool(BaseTool):
    """Json Format Tool."""

    name = "json_format"
    description = "格式化JSON数据"
    input_schema = {
        "type": "object",
        "properties": {
            "input": {
                "type": "string",
                "title": "输入",
                "description": "需要格式化的JSON数据",
            },
            "indent": {
                "type": "integer",
                "title": "缩进",
                "description": "缩进空格数",
                "minimum": 0,
                "maximum": 8,
                "default": 2,
            },
            "sort_keys": {
                "type": "boolean",
                "title": "排序键",
                "description": "是否按键排序",
                "default": False,
            },
        },
        "required": ["input"],
    }
    patterns = [re.compile(r"^[\s]*[\{\[].*[\}\]][\s]*$", re.DOTALL)]
    param_validators = {
        "indent": lambda x: isinstance(x, int) and 0 <= x <= 8,
        "sort_keys": lambda x: isinstance(x, bool),
    }

    def execute(self, params: dict[str, Any]) -> str:
        """Execute the tool."""
        try:
            input_json = json.loads(params.get("input", ""))
            indent = params.get(
                "indent", self.input_schema["properties"]["indent"]["default"]
            )
            sort_keys = params.get(
                "sort_keys", self.input_schema["properties"]["sort_keys"]["default"]
            )

            return json.dumps(
                input_json, indent=indent, sort_keys=sort_keys, ensure_ascii=False
            )
        except json.JSONDecodeError as e:
            return f"JSON格式错误: {str(e)}"
