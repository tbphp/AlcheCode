from venv import logger

from config import State

from .nodes import (
    analyze_node,
    execute_tools_node,
    format_output_node,
    initial_node,
    load_rules_node,
)


class Application:
    is_cli: bool = False
    """是否是命令行模式"""

    state: State
    """应用状态"""

    def __init__(self, input: str, is_cli: bool = False):
        self.is_cli = is_cli
        self.state = State(input=input)

    def run(self) -> str:
        logger.info("Start")

        initial_node(self.state)

        load_rules_node(self.state)

        analyze_node(self.state)

        if self.state.tool_name:
            execute_tools_node(self.state)

        return str(format_output_node(self.state))
