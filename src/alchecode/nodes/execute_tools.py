"""Execute tools node."""

from config import State
from utils import logger

from ..tools import ToolRegistry


def execute_tools_node(state: State):
    """Execute tools node.

    Based on the identified tool type and parameters, calls the corresponding tool to perform operations,
    and stores the result in state.result.

    Args:
        state: Current state object, containing tool type and parameters

    Returns:
        Updated state object, including execution results
    """
    # 检查是否有指定工具名称
    if not state.tool_name:
        state.errors.append("执行工具时未指定工具名称")
        state.result = "错误：未能识别出需要执行的工具"
        return

    try:
        # 获取工具实例
        tools = ToolRegistry.get_tools()
        if state.tool_name not in tools:
            state.errors.append(f"未找到名为'{state.tool_name}'的工具")
            state.result = f"错误：工具'{state.tool_name}'不存在"
            return

        # 创建工具实例并执行
        tool_class = tools[state.tool_name]
        tool_instance = tool_class()

        logger.info(f"执行工具: {state.tool_name}, 参数: {state.params}")

        # 执行工具操作
        result = tool_instance.execute(state.params)

        # 存储结果
        state.result = result
        logger.info(f"工具执行结果: {result[:100]}{'...' if len(result) > 100 else ''}")

    except Exception as e:
        # 记录异常并更新状态
        error_msg = f"执行工具'{state.tool_name}'时发生错误: {str(e)}"
        logger.error(error_msg)
        state.errors.append(error_msg)
        state.result = f"执行出错: {str(e)}"
