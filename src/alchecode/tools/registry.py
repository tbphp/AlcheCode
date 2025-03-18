import json
from typing import LiteralString

from .base import BaseTool


class ToolRegistry:
    """工具自动注册器"""

    _tools: dict[str, type[BaseTool]] = {}

    @classmethod
    def register(cls, tool_class: type[BaseTool]) -> type[BaseTool]:
        """注册工具类"""
        tool_instance = tool_class()
        cls._tools[tool_instance.name] = tool_class
        return tool_class

    @classmethod
    def get_tools(cls) -> dict[str, type[BaseTool]]:
        """工具类key => value列表"""
        return cls._tools

    @classmethod
    def get_tools_list(cls) -> list[BaseTool]:
        """获取工具示例列表"""
        return [tool_class() for tool_class in cls._tools.values()]

    @classmethod
    def format_tool_examples(cls) -> LiteralString:
        """格式化工具提示词"""
        examples = []
        for i, tool in enumerate(cls.get_tools_list(), 1):
            formatted_schema = json.dumps(
                tool.input_schema, indent=2, ensure_ascii=False
            ).replace("\n", "\n    ")
            example = f"""
{i}. {tool.name}
  - Tool Name: {tool.name}
  - Description: {tool.description}
  - Input Schema:
    {formatted_schema}
            """
            examples.append(example)

        return "\n".join(examples)
