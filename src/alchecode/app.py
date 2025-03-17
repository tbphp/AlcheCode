class Application:
    input: str
    """用户输入"""

    is_cli: bool = False
    """是否是命令行模式"""

    def __init__(self, input: str, is_cli: bool = False):
        self.input = input
        self.is_cli = is_cli

    def run(self) -> str:
        return self.input
