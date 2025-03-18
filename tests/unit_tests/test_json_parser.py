import json

import pytest

from utils.json_parser import parse_llm_json


def test_parse_plain_json():
    """测试解析普通JSON字符串"""
    json_str = '{"name": "test", "value": 123}'
    result = parse_llm_json(json_str)
    assert result == {"name": "test", "value": 123}


def test_parse_markdown_json():
    """测试从markdown代码块中解析JSON"""
    markdown_str = """
    这是一些说明文字
    ```json
    {
        "name": "test",
        "value": 123
    }
    ```
    这是后续文字
    """
    result = parse_llm_json(markdown_str)
    assert result == {"name": "test", "value": 123}


def test_parse_json_with_comments():
    """测试从带有额外文本的内容中解析JSON"""
    text_with_json = """
    根据分析结果：
    {"tool": "example", "confidence": 0.95}
    希望这个结果对您有帮助
    """
    result = parse_llm_json(text_with_json)
    assert result == {"tool": "example", "confidence": 0.95}


def test_parse_invalid_json():
    """测试解析无效JSON时的错误处理"""
    with pytest.raises(json.JSONDecodeError):
        parse_llm_json("这不是一个JSON字符串")


def test_parse_multiple_json_blocks():
    """测试当存在多个JSON块时，使用第一个有效的JSON"""
    multiple_blocks = """
    ```json
    {"first": true, "input": {"test": 123}}
    ```
    其他内容
    ```json
    {"second": true}
    ```
    """
    result = parse_llm_json(multiple_blocks)
    assert result == {"first": True, "input": {"test": 123}}


def test_parse_array_json():
    """测试解析JSON数组"""
    array_str = """
    一些文本
    [1, 2, 3, {"test": "value", "input": {"test": 123}}]
    更多文本
    """
    result = parse_llm_json(array_str)
    assert result == [1, 2, 3, {"test": "value", "input": {"test": 123}}]


def test_parse_object_json():
    """测试解析嵌套对象的JSON"""
    nested_object = """
    一些文本
    ```json
    {
        "name": "test",
        "value": {
            "nested": true
        }
    }
    ```
    """
    result = parse_llm_json(nested_object)
    assert result == {"name": "test", "value": {"nested": True}}
