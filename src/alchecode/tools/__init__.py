import importlib
import inspect
import os
import pkgutil

from utils import logger

from .base import BaseTool
from .registry import ToolRegistry


def tool(cls: type[BaseTool]) -> type[BaseTool]:
    """工具装饰器"""
    if not inspect.isclass(cls):
        raise TypeError("@tool装饰器只能用于BaseTool的子类")
    return ToolRegistry.register(cls)


def discover_tools(package_path: str = "alchecode.tools") -> None:
    """工具自动发现"""
    package = importlib.import_module(package_path)
    package_file = package.__file__
    if package_file is None:
        logger.error(f"无法确定包{package_path}的目录路径")
        return

    package_dir = os.path.dirname(package_file)

    for _, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
        if not is_pkg and module_name not in ["base", "registry", "__init__"]:
            module_path = f"{package_path}.{module_name}"
            try:
                importlib.import_module(module_path)
            except Exception as e:
                logger.error(f"导入模块{module_path}时出错: {e}")


__all__ = ["ToolRegistry"]
