"""Analyzer for EngineeredPrompts."""

import json
import pathlib
from typing import Dict, List

from promptarchitect.prompting import EngineeredPrompt


class EngineeredPromptAnalyzer:
    """Analyze EngineeredPrompts."""

    def __init__(self) -> None:
        base_path = (
            pathlib.Path(__file__).parent.parent
            / "analyzer"
            / "analyze_test_cases.prompt"
        )
        self.test_case_suggestions_prompt = str(base_path)
        self.test_case_suggestions = []

    def analyze_test_cases(self, prompt_file: str) -> List[Dict]:
        """Analyze test cases for an EngineeredPrompt.

        Arguments
        ---------
        prompt_file: str
            The path to the prompt file to analyze.
        """
        input_prompt = EngineeredPrompt(prompt_file=prompt_file)

        metadata = input_prompt.specification.metadata

        # Check if the prompt file has test cases defined
        if len(metadata.tests) == 0:
            return []

        analysis_prompt = EngineeredPrompt(
            prompt_file=self.test_case_suggestions_prompt,
        )
        # Construct the test case text
        test_cases = ""
        if metadata.tests is not None:
            for key, value in metadata.tests.items():
                test_cases += f"{key}: {str(value.model_dump())}\n"

        # Fill in the template properties in the analysis prompt
        properties = {
            "prompt_specification": test_cases,
            "prompt_text": input_prompt.specification.prompt,
        }

        response = analysis_prompt.run(input_file=prompt_file, properties=properties)
        self.test_case_suggestions = json.loads(response)

        return self.test_case_suggestions
