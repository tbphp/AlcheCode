"""Base tool class."""

from abc import ABC, abstractmethod
from re import Match
from typing import Any, Pattern


class BaseTool(ABC):
    """Base tool class."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> dict[str, Any]:
        """Input schema."""
        pass

    @property
    @abstractmethod
    def patterns(self) -> list[Pattern[str]]:
        """Regular expression patterns."""
        pass

    @property
    def param_validators(self) -> dict[str, Any]:
        """Parameter validators."""
        return {}

    def extract_params(self, index: int, match: Match[str]) -> dict[str, Any]:
        """Extract params from match object."""
        return {}

    @abstractmethod
    def execute(self, params: dict[str, Any]) -> str:
        """Execute tool."""
        pass

    def match(self, input_text: str) -> tuple[bool, dict[str, Any]]:
        """Check if input text matches any pattern."""
        for i, pattern in enumerate(self.patterns):
            match = pattern.match(input_text)
            if match:
                params = self.extract_params(i, match)
                return True, params
        return False, {}
