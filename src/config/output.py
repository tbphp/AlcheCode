import json
from dataclasses import dataclass, field

from config.enums import StatusEnum


@dataclass
class Output:
    tool_name: str = field(default="", metadata={"description": "工具名称"})
    """工具名称"""

    result: str = field(default="", metadata={"description": "执行结果"})
    """执行结果"""

    corrections: list[dict[str, str]] = field(
        default_factory=list,
        metadata={"description": "输入修正建议列表，包含original和corrected字段"},
    )
    """输入修正建议列表，包含original和corrected字段"""

    status: int = field(
        default=StatusEnum.SUCCESS.value, metadata={"description": "执行状态枚举"}
    )
    """执行状态枚举"""

    status_message: str = field(
        default=StatusEnum.SUCCESS.name.lower().capitalize(),
        metadata={"description": "执行状态信息"},
    )
    """执行状态信息"""

    errors: list[str] = field(
        default_factory=list, metadata={"description": "错误信息列表"}
    )
    """错误信息列表"""

    def __str__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
