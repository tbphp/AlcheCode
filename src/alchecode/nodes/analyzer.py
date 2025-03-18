import json
from typing import Any

from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

from config import Config, State
from config.prompts import INTENT_ANALYSIS_PROMPT
from utils import logger, parse_llm_json

from ..tools.registry import ToolRegistry


def apply_user_rules(state: State) -> bool:
    """使用用户规则"""
    input_text = state.input.strip()

    if input_text in state.rules:
        state.input = state.rules[input_text]
        return True

    for rule_key, rule_value in state.rules.items():
        if input_text.startswith(rule_key + " "):
            params = input_text[len(rule_key) :].strip()
            state.input = f"{rule_value} {params}"
            return True

    return False


def detect_tool_by_regex(input_text: str) -> tuple[str | None, dict[str, Any]]:
    """使用正则表达式模式检测工具类型和参数"""
    for tool in ToolRegistry.get_tools_list():
        is_match, params = tool.match(input_text)
        if is_match:
            return tool.name, params
    return None, {}


def detect_json_data(input_text: str) -> tuple[bool, dict[str, Any] | None]:
    """检测输入文本中的JSON数据"""
    try:
        input_text = input_text.strip()
        if not (input_text.startswith("{") or input_text.startswith("[")):
            return False, None
        data = json.loads(input_text)
        return True, data
    except json.JSONDecodeError:
        if ("{" in input_text and "}" in input_text) or (
            "[" in input_text and "]" in input_text
        ):
            return True, None
        return False, None


def analyze_with_llm(state: State) -> None:
    """使用LLM分析用户意图"""
    try:
        tool_examples = ToolRegistry.format_tool_examples()
        logger.info(f"Analyzing tool examples:{tool_examples}")

        llm = init_chat_model(Config.model, temperature=0)
        prompt = ChatPromptTemplate([("human", INTENT_ANALYSIS_PROMPT)])

        response = prompt.pipe(llm).invoke(
            {
                "tool_examples": tool_examples,
                "user_input": state.input,
                "confidence_threshold": Config.confidence_threshold,
                "language": Config.llm_language,
            }
        )

        logger.info(f"LLM analysis response: \n{str(response.content)}\n")

        try:
            analysis = parse_llm_json(str(response.content))
            state.confidence = float(analysis.get("confidence", 0))
            tool_name = analysis.get("tool_name", "")

            # 检查置信度
            if state.confidence < Config.confidence_threshold:
                state.result = analysis.get(
                    "output", "Analysis confidence below threshold"
                )
                state.errors.append(f"Confidence too low: {state.confidence}")
                return

            # 检查是否识别到工具
            if not tool_name:
                state.result = analysis.get("output", "No tool identified")
                state.errors.append("No tool identified")
                return

            # 工具存在且置信度足够高
            if tool_name in ToolRegistry.get_tools():
                state.tool_name = tool_name
                state.params.update(analysis.get("params", {}))
                if "corrections" in analysis:
                    state.corrections = analysis["corrections"]
            else:
                state.result = analysis.get("output", f"Tool {tool_name} not found")
                state.errors.append(f"Identified tool '{tool_name}' not available")

        except json.JSONDecodeError:
            state.errors.append("LLM返回的内容无法解析为JSON格式")
            state.result = "分析失败：无法解析结果"
        except KeyError as e:
            state.errors.append(f"LLM分析结果缺少关键字段: {str(e)}")
            state.result = "分析失败：结果格式不完整"

    except Exception as e:
        logger.error(f"LLM analysis error: {str(e)}")
        state.errors.append(f"LLM分析过程发生错误: {str(e)}")
        state.result = "分析过程中发生意外错误"


def validate_and_apply_defaults(state: State) -> None:
    """验证工具参数"""
    # 验证工具是否存在
    tools = ToolRegistry.get_tools()
    if not state.tool_name or state.tool_name not in tools:
        return
    tool = tools[state.tool_name]()

    properties = tool.input_schema.get("properties", {})

    # 辅助函数：获取参数默认值
    def get_default(param_name: str) -> Any:
        return properties.get(param_name, {}).get("default", None)

    for param_name, prop in properties.items():
        if "default" in prop and param_name not in state.params:
            state.params[param_name] = prop["default"]

    invalid_params = []
    for param_name, validator in tool.param_validators.items():
        if param_name not in state.params:
            continue

        if not callable(validator) or not validator(state.params[param_name]):
            invalid_params.append(param_name)
            state.params[param_name] = get_default(param_name)

    if invalid_params:
        state.errors.append(f"Invalid parameters reset: {', '.join(invalid_params)}")


def analyze_node(state: State) -> None:
    """分析节点

    该节点用于分析用户输入，识别意图并提取参数。
    该节点实现了多层次的意图识别策略：
    1. 首先应用用户自定义规则
    2. 使用正则表达式进行模式匹配
    3. 如果上述方法无法确定意图，则使用LLM进行分析
    """
    # 第一层：应用用户自定义规则
    apply_user_rules(state)

    # 第一层：正则表达式模式匹配
    tool_name, params = detect_tool_by_regex(state.input)
    if tool_name:
        state.tool_name = tool_name
        state.params = params
        state.confidence = 1.0
        validate_and_apply_defaults(state)
        return

    # 第二层：如果简单策略无法识别，使用LLM
    if not state.tool_name or state.confidence < Config.confidence_threshold:
        analyze_with_llm(state)

    # 第三层：参数验证与默认值应用
    validate_and_apply_defaults(state)
