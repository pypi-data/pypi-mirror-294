import pytest
from dotenv import load_dotenv
from promptarchitect.claude_completion import ClaudeCompletion

load_dotenv()


@pytest.mark.llm()
def test_completion():
    completion = ClaudeCompletion("You're a friendly assistant.")
    prompt = "What is the capital of France?"

    response = completion.completion(prompt)

    assert response is not None


@pytest.mark.llm()
def test_assign_parameters():
    parameters = {"temperature": 0.7, "top_p": 0.9}
    completion = ClaudeCompletion("You're a friendly assistant.", parameters=parameters)

    assert completion.parameters == parameters
    assert completion.model == "claude-3-5-sonnet-20240620"


@pytest.mark.llm()
def test_cost_and_duration():
    completion = ClaudeCompletion("You're a friendly assistant.")
    prompt = "What is the capital of France?"

    completion.completion(prompt)

    assert completion.cost is not None
    assert completion.duration is not None


@pytest.mark.llm()
def test_model_alias():
    completion = ClaudeCompletion(
        "You're a friendly assistant.",
        model="claude-3-5-sonnet",
    )
    assert completion.model == "claude-3-5-sonnet-20240620"


@pytest.mark.llm()
def test_model_unknown_alias():
    expected_error_message = (
        "Model claude-1.0 not supported. Check the provider file anthropic.json."
    )

    with pytest.raises(ValueError, match=expected_error_message):
        ClaudeCompletion("You're a friendly assistant.", model="claude-1.0")


@pytest.mark.llm()
def test_run_with_parameters():
    parameters = {"temperature": 0.1, "top_p": 0.1, "max_tokens": 10}
    completion = ClaudeCompletion("You're a friendly assistant.", parameters=parameters)

    response = completion.completion("What is the capital of France?")

    assert completion.parameters == parameters
    assert response is not None
    assert "Paris" in response
    assert completion.input_tokens is not None
    assert completion.output_tokens is not None
    assert completion.cost is not None

@pytest.mark.llm()
def test_run_with_parameters_containing_none_values():
    parameters = {"temperature": None, "top_p": None, "max_tokens": None}
    completion = ClaudeCompletion("You're a friendly assistant.", parameters=parameters)

    response = completion.completion("What is the capital of France?")

    assert completion.parameters == parameters
    assert response is not None
    assert "Paris" in response
    assert completion.input_tokens is not None
    assert completion.output_tokens is not None
    assert completion.cost is not None
