from ..models import EvaluationLog


def save_evaluation_log(
    lesson_run,
    attempt_number: int,
    evaluation,
    failed_checks: list[str],
    regeneration_feedback: list[str],
    changes_made: list[str] | None = None,
):
    return EvaluationLog.objects.create(
        lesson_run=lesson_run,
        attempt_number=attempt_number,
        passed=len(failed_checks) == 0,
        evaluation=evaluation.model_dump(),
        failed_checks=failed_checks,
        regeneration_feedback=regeneration_feedback,
        changes_made=changes_made or [],
    )


def build_rejection_log(lesson_run) -> list[dict]:
    logs = lesson_run.evaluations.all()

    rejection_log = []

    for log in logs:

        if log.passed:
            status = "PASSED"
        else:
            status = "REJECTED"

        rejection_log.append(
            {
                "attempt": log.attempt_number,
                "status": status,
                "failed_checks": log.failed_checks,
                "feedback": log.regeneration_feedback,
                "changes_made": log.changes_made,
            }
        )

    return rejection_log