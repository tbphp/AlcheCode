"""Load rules node."""

from pathlib import Path

from config import State


def load_rules_node(state: State) -> None:
    """Load the rules.txt rules."""
    try:
        # 加载用户规则
        rule_file = Path("rules.txt")
        if not rule_file.exists():
            return

        with rule_file.open("r", encoding="utf-8") as f:
            for _, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                state.rules[key] = value

        # 验证合法性
        invalid_rules = [k for k in state.rules if not k.isidentifier()]
        if invalid_rules:
            state.errors.append(f"非法规则名称: {', '.join(invalid_rules)}")
            state.rules = {}
    except UnicodeDecodeError as e:
        state.errors.append(f"编码错误: {str(e)}")
    except PermissionError:
        state.errors.append("无权限读取规则文件")
    except Exception as e:
        state.errors.append(f"规则加载失败: {str(e)}")
