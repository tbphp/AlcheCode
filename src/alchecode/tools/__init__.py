"""Tools package."""

import importlib
import inspect
import os
import pkgutil

from utils import logger

from .base import BaseTool
from .registry import ToolRegistry


def tool(cls: type[BaseTool]) -> type[BaseTool]:
    """Tool decorator."""
    if not inspect.isclass(cls) or not issubclass(cls, BaseTool):
        raise TypeError("@tool装饰器只能用于BaseTool的子类")
    return ToolRegistry.register(cls)


def discover_tools(package_path: str = "alchecode.tools"):
    """Discover tools."""
    package = importlib.import_module(package_path)
    package_dir = os.path.dirname(package.__file__)

    for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
        if not is_pkg and module_name not in ["base", "registry", "__init__"]:
            module_path = f"{package_path}.{module_name}"
            try:
                importlib.import_module(module_path)
            except Exception as e:
                logger.error(f"导入模块{module_path}时出错: {e}")
