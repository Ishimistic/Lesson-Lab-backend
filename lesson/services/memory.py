from ..models import Memory


def build_memory_context(limit: int = 10) -> str:
    memories = Memory.objects.order_by(
        "-occurrence_count",
        "-updated_at",
    )[:limit]

    if not memories:
        return "No previous lessons learned."


    lines = [
        "Lessons learned from previous runs:"
    ]

    for memory in memories:
        lines.append(
            f"- {memory.failure_type}: "
            f"{memory.lesson_learned}"
        )

    return "\n".join(lines)


def update_memory(
    failed_checks: list[str],
    feedback: dict,
) -> None:

    for failure_type in failed_checks:

        failure_feedback = feedback.get(
            failure_type,
            "Improve this criterion in future generations.",
        )

        memory, created = Memory.objects.get_or_create(
            failure_type=failure_type,
            defaults={
                "lesson_learned": failure_feedback,
                "occurrence_count": 1,
            },
        )

        if not created:
            memory.lesson_learned = failure_feedback
            memory.occurrence_count += 1
            memory.save(
                update_fields=[
                    "lesson_learned",
                    "occurrence_count",
                    "updated_at",
                ]
            )