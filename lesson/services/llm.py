from django.conf import settings
from langchain_groq import ChatGroq


def get_llm(
    temperature: float = 0.0,
) -> ChatGroq:

    if not settings.GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    return ChatGroq(
        model=settings.LLM_MODEL,
        groq_api_key=settings.GROQ_API_KEY,
        temperature=temperature,
        max_tokens=4096,
        timeout=60,
        max_retries=2,
    )