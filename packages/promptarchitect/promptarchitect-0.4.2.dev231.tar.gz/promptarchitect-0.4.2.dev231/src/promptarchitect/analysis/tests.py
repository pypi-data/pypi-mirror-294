"""Test case analysis for prompt files."""

from pathlib import Path

from promptarchitect.analysis.core import Analyzer
from promptarchitect.prompting import EngineeredPrompt


class TestAnalyzer(Analyzer):
    """Analyze the tests in an engineered prompt file."""

    def __init__(self) -> None:
        super().__init__()

        self.prompt_path = (
            Path(__file__).parent.parent
            / "analysis"
            / "prompts"
            / "analyze_test_cases.prompt"
        )

    def run(self, prompt_file: str) -> str:
        """Analyze test cases for an EngineeredPrompt.

        Arguments
        ---------
        prompt_file: str
            The path to the prompt file to analyze.
        """
        input_prompt = EngineeredPrompt(prompt_file=prompt_file)

        metadata = input_prompt.specification.metadata

        if len(metadata.tests) == 0:
            return "No tests found in the prompt file."

        analysis_prompt = EngineeredPrompt(
            prompt_file=self.prompt_path,
        )

        test_cases = ""

        if metadata.tests is not None:
            for key, value in metadata.tests.items():
                test_cases += f"{key}: {str(value.model_dump())}\n"

        properties = {
            "prompt_specification": test_cases,
            "prompt_text": input_prompt.specification.prompt,
        }

        return analysis_prompt.run(input_file=prompt_file, properties=properties)
