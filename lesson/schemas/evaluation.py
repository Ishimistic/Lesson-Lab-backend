from pydantic import BaseModel, Field


class RubricCheck(BaseModel):
    passed: bool = Field(
        description="Whether the criterion passes."
    )

    reason: str = Field(
        description="Why the criterion passed or failed."
    )

    feedback: str = Field(
        description=(
            "Specific instruction for improving the lesson. "
            "If the criterion passed, explain what should be preserved."
        )
    )


class EvaluationResult(BaseModel):
    accuracy: RubricCheck

    beginner_friendly: RubricCheck

    examples: RubricCheck

    jargon: RubricCheck

    coverage: RubricCheck

    flow: RubricCheck