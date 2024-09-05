"""Tests for PsiEngineeredPromptAnalyzer"""

import pytest
from promptarchitect.analyzer.psi_prompt_analyzer import PsiEngineeredPromptAnalyzer


@pytest.mark.llm()
def test_analyze_test_cases():
    analyzer = PsiEngineeredPromptAnalyzer()
    psi_and_recommendations = analyzer.analyze_prompts(
        prompt_file_path=str("tests/analyzer/article.prompt"),
    )

    assert psi_and_recommendations is not None


@pytest.mark.llm()
def test_no_tests():
    analyzer = PsiEngineeredPromptAnalyzer()
    psi_and_recommendations = analyzer.analyze_prompts(
        prompt_file_path=str("tests/analyzer/no_tests.prompt"),
    )

    assert psi_and_recommendations is not None
