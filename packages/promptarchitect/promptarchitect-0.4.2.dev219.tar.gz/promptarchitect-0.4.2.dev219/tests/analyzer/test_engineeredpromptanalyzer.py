"""Tests for EngineeredPromptAnalyzer"""

import pytest
from promptarchitect.analyzer.engineeredpromptanalyzer import EngineeredPromptAnalyzer


@pytest.mark.llm()
def test_analyze_test_cases():
    analyzer = EngineeredPromptAnalyzer()
    suggestions = analyzer.analyze_test_cases(
        prompt_file=str("tests/analyzer/article.prompt"),
    )

    assert suggestions[0]["test_id"] == "test_01"
    assert suggestions[0]["description"] is not None
    assert suggestions[0]["score"] > 0
    assert suggestions[0]["score"] <= 5
    assert suggestions[0]["analysis"] is not None
    assert suggestions[0]["recommendations"] is not None

    assert suggestions[1]["test_id"] == "test_02"


def test_no_tests():
    analyzer = EngineeredPromptAnalyzer()
    suggestions = analyzer.analyze_test_cases(
        prompt_file=str("tests/analyzer/no_tests.prompt"),
    )

    assert suggestions == []
