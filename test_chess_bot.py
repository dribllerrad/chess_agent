from chess_bot import query_rag
from set_llm import set_llm
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response qualitatively match the expected response in a geneeral way? 
"""


def test_chess_board_size():
    assert query_and_validate(
        question="How many squares are on a chess board? Verbose=OFF. Be concise and answer with a single integer value.",
        expected_response="64",
    )

def test_chess_piece_king():
    assert query_and_validate(
        question="Is the King a chess piece?  Answer yes or no",
        expected_response="yes",
    )

def test_chess_piece_pope():
    assert query_and_validate(
        question="Is the Pope a chess piece?  Answer yes or no",
        expected_response="no",
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = set_llm()
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
