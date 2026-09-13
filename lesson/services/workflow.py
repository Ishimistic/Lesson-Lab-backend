import json
from pathlib import Path

from django.conf import settings

from ..models import LessonRun

from .evaluator import (
    evaluate_lesson,
    evaluation_passed,
    get_failed_checks,
    get_regeneration_feedback,
)

from .generator import generate_lesson

from .logger import (
    build_rejection_log,
    save_evaluation_log,
)

from .memory import (
    build_memory_context,
    update_memory,
)


def _inject_demo_error(lesson: str) -> str:
    return (
        lesson
        + "\n\n"
        + "### Deliberate Demo Error\n\n"
        + "RAG retrains the AI model every time a user "
          "asks a question, permanently teaching the model "
          "the retrieved information."
    )


def _build_feedback_dict(evaluation) -> dict:

    return {
        "accuracy": evaluation.accuracy.feedback,
        "beginner_friendly": evaluation.beginner_friendly.feedback,
        "examples": evaluation.examples.feedback,
        "jargon": evaluation.jargon.feedback,
        "coverage": evaluation.coverage.feedback,
        "flow": evaluation.flow.feedback,
    }


def _save_output_files(
    lesson_run,
    lesson: str,
) -> None:

    output_dir = Path(settings.BASE_DIR) / "outputs"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    final_lesson_path = (
        output_dir / "final_lesson.md"
    )

    rejection_log_path = (
        output_dir / "rejection_log.json"
    )

    final_lesson_path.write_text(
        lesson,
        encoding="utf-8",
    )

    rejection_log = build_rejection_log(
        lesson_run
    )

    rejection_log_path.write_text(
        json.dumps(
            {
                "topic": lesson_run.topic,
                "status": lesson_run.status,
                "attempts": lesson_run.attempts,
                "attempts_detail": rejection_log,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def run_lesson_workflow(topic: str,  inject_demo_error: bool = False,) -> dict:

    lesson_run = LessonRun.objects.create(
        topic=topic,
        status=LessonRun.STATUS_RUNNING,
    )

    memory_context = build_memory_context()

    lesson = generate_lesson(
        topic=topic,
        memory_context=memory_context,
    )

    if inject_demo_error:
        lesson = _inject_demo_error(lesson)

    max_attempts = settings.MAX_LESSON_RETRIES + 1

    for attempt in range(1, max_attempts + 1):

        evaluation = evaluate_lesson(
            topic=topic,
            lesson=lesson,
        )

        passed = evaluation_passed(
            evaluation
        )

        failed_checks = get_failed_checks(
            evaluation
        )

        regeneration_feedback = (
            get_regeneration_feedback(
                evaluation
            )
        )

        evaluation_log = save_evaluation_log(
            lesson_run=lesson_run,
            attempt_number=attempt,
            evaluation=evaluation,
            failed_checks=failed_checks,
            regeneration_feedback=regeneration_feedback,
        )

        lesson_run.attempts = attempt
        lesson_run.final_lesson = lesson
        lesson_run.save(
            update_fields=[
                "attempts",
                "final_lesson",
                "updated_at",
            ]
        )

        if passed:

            lesson_run.status = (
                LessonRun.STATUS_PASSED
            )

            lesson_run.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            _save_output_files(
                lesson_run=lesson_run,
                lesson=lesson,
            )

            return {
                "status": "passed",
                "topic": topic,
                "attempts": attempt,
                "lesson": lesson,
                "rejection_log": build_rejection_log(
                    lesson_run
                ),
            }

        feedback_dict = _build_feedback_dict(
            evaluation
        )

        update_memory(
            failed_checks=failed_checks,
            feedback=feedback_dict,
        )

        if attempt == max_attempts:

            lesson_run.status = (
                LessonRun.STATUS_FAILED
            )

            lesson_run.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            _save_output_files(
                lesson_run=lesson_run,
                lesson=lesson,
            )

            return {
                "status": "failed",
                "topic": topic,
                "attempts": attempt,
                "lesson": lesson,
                "rejection_log": build_rejection_log(
                    lesson_run
                ),
            }

        updated_memory_context = (
            build_memory_context()
        )

        feedback_text = "\n".join(
            regeneration_feedback
        )
        
        previous_lesson = lesson

        lesson = generate_lesson(
            topic=topic,
            memory_context=updated_memory_context,
            feedback=feedback_text,
            previous_lesson=lesson,
        )
        
        changes_made = [
            f"Regenerated the lesson to fix:: {feedback}"
            for feedback in regeneration_feedback
        ]
        
        evaluation_log.changes_made = changes_made
        evaluation_log.save(
            update_fields=["changes_made"]
        )

    raise RuntimeError(
        "Workflow terminated unexpectedly."
    )