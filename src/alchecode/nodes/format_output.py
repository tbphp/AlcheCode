from config import Output, State
from config.enums import StatusEnum


def format_output_node(state: State) -> Output:
    """格式化输出节点"""
    # 构建基础输出结构
    output = Output(
        tool_name=state.tool_name,
        result=state.result,
        corrections=state.corrections,
        errors=[],
    )

    # 处理错误信息（优先级最高）
    if state.errors:
        status = StatusEnum.ERROR
        output.errors = state.errors
    # 正常执行结果
    else:
        status = StatusEnum.DIRECT if not state.tool_name else StatusEnum.SUCCESS

    output.status = status.value
    output.status_message = status.name.lower()
    return output
