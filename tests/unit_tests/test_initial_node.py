import pytest

from alchecode.nodes import initial_node
from config import State


class TestInitialNode:
    def test_empty_input(self) -> None:
        state = State("")
        with pytest.raises(OSError) as e:
            initial_node(state)
        assert "EMPTY_INPUT" in str(e.value)

    def test_exceed_length(self) -> None:
        large_input = "a" * (10 * 1024 * 1024 + 1)
        state = State(large_input)
        with pytest.raises(OSError) as e:
            initial_node(state)
        assert "EXCEED_LENGTH_LIMIT" in str(e.value)

    def test_normalization(self) -> None:
        state = State("  Hello\n\rWorld  \r\n")
        initial_node(state)
        assert state.input == "Hello\nWorld"

    def test_injection_detection(self) -> None:
        state = State("${test} <?php code ?> `command`")
        with pytest.raises(OSError) as e:
            initial_node(state)
        assert "INVALID_ENCODING" in str(e.value)
