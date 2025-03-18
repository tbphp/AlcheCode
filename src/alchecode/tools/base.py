"""Base tool class."""

from abc import ABC, abstractmethod
from re import Match
from typing import Any, Pattern


class BaseTool(ABC):
    """工具基础类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """工具名称"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """工具描述"""
        pass

    @property
    def input_schema(self) -> dict[str, Any]:
        """输入参数表"""
        return {}

    @property
    def patterns(self) -> list[Pattern[str]]:
        """正则列表"""
        return []

    @property
    def param_validators(self) -> dict[str, Any]:
        """参数校验"""
        return {}

    def extract_params(self, index: int, match: Match[str]) -> dict[str, Any]:
        """从匹配对象中提取参数。"""
        return {}

    @abstractmethod
    def execute(self, params: dict[str, Any]) -> str:
        """执行工具方法"""
        pass

    def match(self, input_text: str) -> tuple[bool, dict[str, Any]]:
        """正则匹配"""
        for i, pattern in enumerate(self.patterns):
            match = pattern.match(input_text)
            if match:
                params = self.extract_params(i, match)
                return True, params
        return False, {}
