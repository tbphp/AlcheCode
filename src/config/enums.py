from enum import Enum, auto


class StatusEnum(Enum):
    """状态枚举类"""

    SUCCESS = auto()
    """成功"""

    ERROR = auto()
    """错误"""

    DIRECT = auto()
    """LLM直接返回结果"""
