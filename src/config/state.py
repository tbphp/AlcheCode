import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class State:
    input: str

    rules: dict[str, str] = field(
        default_factory=dict, metadata={"description": "用户自定义规则映射表"}
    )

    tool_name: str = field(default="", metadata={"description": "识别出的工具类型"})

    params: dict[str, Any] = field(
        default_factory=dict, metadata={"description": "工具参数字典"}
    )

    corrections: list[dict[str, str]] = field(
        default_factory=list,
        metadata={"description": "输入修正建议列表，包含original和corrected字段"},
    )

    confidence: float = field(
        default=0.0, metadata={"description": "意图识别的置信度，0到1之间"}
    )

    errors: list[str] = field(
        default_factory=list, metadata={"description": "错误信息列表"}
    )

    result: str = field(default="", metadata={"description": "工具执行结果"})

    def __str__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
