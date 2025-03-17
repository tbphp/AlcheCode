"""Tool Registry."""

import json
from typing import LiteralString

from .base import BaseTool


class ToolRegistry:
    """Tool registry."""

    _tools: dict[str, type[BaseTool]] = {}

    @classmethod
    def register(cls, tool_class: type[BaseTool]) -> type[BaseTool]:
        """Register tool class."""
        tool_instance = tool_class()
        cls._tools[tool_instance.name] = tool_class
        return tool_class

    @classmethod
    def get_tool(cls, tool_name: str) -> type[BaseTool]:
        """Get tool class by name."""
        return cls._tools.get(tool_name)

    @classmethod
    def get_tools(cls) -> dict[str, type[BaseTool]]:
        """Get all tool instances."""
        return cls._tools

    @classmethod
    def get_tools_list(cls) -> list[BaseTool]:
        """Get all tool instances."""
        return [tool_class() for tool_class in cls._tools.values()]

    @classmethod
    def format_tool_examples(cls) -> LiteralString:
        """Format tools into examples for prompt."""
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
