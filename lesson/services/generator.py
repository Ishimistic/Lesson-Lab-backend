from langchain_core.prompts import ChatPromptTemplate
from django.conf import settings

from ..prompts.generator import (
    GENERATOR_HUMAN_PROMPT,
    GENERATOR_SYSTEM_PROMPT,
)

from .llm import get_llm


def _build_generator_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                GENERATOR_SYSTEM_PROMPT,
            ),
            (
                "human",
                GENERATOR_HUMAN_PROMPT,
            ),
        ]
    )

    llm = get_llm(temperature=0.3)

    return prompt | llm


def generate_lesson(
    topic: str,
    memory_context: str,
    feedback: str = "",
    previous_lesson: str = "",
) -> str:

    chain = _build_generator_chain()

    response = chain.invoke(
        {
            "topic": topic,
            "memory_context": memory_context,
            "feedback": feedback or "No previous feedback.",
            "previous_lesson": (
                previous_lesson
                or "No previous lesson. This is the first attempt."
            ),
        }
    )

    return response.content.strip()