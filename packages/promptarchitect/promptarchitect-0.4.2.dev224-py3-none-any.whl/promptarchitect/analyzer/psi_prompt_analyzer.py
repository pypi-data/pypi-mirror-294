"""PSI Analyzer and recommender for EngineeredPrompts."""

import pathlib

from promptarchitect.prompting import EngineeredPrompt


class PsiEngineeredPromptAnalyzer:
    """Analyze EngineeredPrompts using the Prompt Specification Index (PSI).

    The PSI score is calculated using the following metrics:
        1. Complexity (25% weight): How intricate or nuanced the prompt is (scale 1-10)
        3. Wordiness (15% weight): How verbose or concise the prompt is relative to
        its content (scale 1-10)
        4. Defined Tests (40% weight): The number of specific tests or criteria
        included to validate the AI's output (count)

    The PSI score ranges from 0 to 10, with higher scores indicating more
    sophisticated prompts.

    This analysis is performed using a LLM model as specific in the
    psi_prompt_recommendations.prompt file.
    """

    def __init__(self) -> None:
        base_path = (
            pathlib.Path(__file__).parent.parent
            / "analyzer"
            / "psi_prompt_recommendations.prompt"
        )
        self.psi_analysis_prompt = str(base_path)

    def analyze_prompts(self, prompt_file_path: str) -> str:
        """Analyze test cases for an EngineeredPrompt.

        This function analyzes an EngineeredPrompt and returns the Prompt Sophistication
         Index (PSI) score and gives recommendations on how to improve your prompt
         based on the metrics used within the PSI score.

        Arguments
        ---------
        prompt_file: str
            The path to the prompt file to analyze.
        """
        prompt_filename = pathlib.Path(prompt_file_path).stem

        analysis_prompt = EngineeredPrompt(
            prompt_file=self.psi_analysis_prompt,
            output_path="src/promptarchitect/analyzer/output/",
        )
        analysis_prompt.specification.metadata.output = (
            f"psi_report_{prompt_filename}.md"
        )

        with open(prompt_file_path, "r") as file:
            prompt_file = file.read()

        return analysis_prompt.run(input_text=prompt_file)

