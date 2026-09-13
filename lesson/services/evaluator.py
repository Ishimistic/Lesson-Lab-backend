from langchain_core.prompts import ChatPromptTemplate

from ..prompts.evaluator import EVALUATOR_SYSTEM_PROMPT
from ..schemas.evaluation import EvaluationResult

from .llm import get_llm


EVALUATOR_HUMAN_PROMPT = """
Evaluate the following lesson.

TOPIC
-----
{topic}

LESSON
------
{lesson}
"""


def _build_evaluator_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                EVALUATOR_SYSTEM_PROMPT,
            ),
            (
                "human",
                EVALUATOR_HUMAN_PROMPT,
            ),
        ]
    )

    llm = get_llm(
        temperature=0.0,
    )

    structured_llm = llm.with_structured_output(
        EvaluationResult,
        method="json_schema",
    )

    return prompt | structured_llm


def evaluate_lesson(
    topic: str,
    lesson: str,
) -> EvaluationResult:

    chain = _build_evaluator_chain()

    return chain.invoke(
        {
            "topic": topic,
            "lesson": lesson,
        }
    )


def evaluation_passed(
    evaluation: EvaluationResult,
) -> bool:

    return all(
        [
            evaluation.accuracy.passed,
            evaluation.beginner_friendly.passed,
            evaluation.examples.passed,
            evaluation.jargon.passed,
            evaluation.coverage.passed,
            evaluation.flow.passed,
        ]
    )


def get_failed_checks(
    evaluation: EvaluationResult,
) -> list[str]:

    checks = {
        "accuracy": evaluation.accuracy,
        "beginner_friendly": evaluation.beginner_friendly,
        "examples": evaluation.examples,
        "jargon": evaluation.jargon,
        "coverage": evaluation.coverage,
        "flow": evaluation.flow,
    }

    return [
        name
        for name, result in checks.items()
        if not result.passed
    ]


def get_regeneration_feedback(
    evaluation: EvaluationResult,
) -> list[str]:

    checks = {
        "accuracy": evaluation.accuracy,
        "beginner_friendly": evaluation.beginner_friendly,
        "examples": evaluation.examples,
        "jargon": evaluation.jargon,
        "coverage": evaluation.coverage,
        "flow": evaluation.flow,
    }

    return [
        f"{name}: {result.feedback}"
        for name, result in checks.items()
        if not result.passed
    ]