from django.db import models


class LessonRun(models.Model):
    STATUS_RUNNING = "running"
    STATUS_PASSED = "passed"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_RUNNING, "Running"),
        (STATUS_PASSED, "Passed"),
        (STATUS_FAILED, "Failed"),
    ]

    topic = models.CharField(max_length=255)

    final_lesson = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_RUNNING,
    )

    attempts = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - {self.status}"


class EvaluationLog(models.Model):
    lesson_run = models.ForeignKey(
        LessonRun,
        on_delete=models.CASCADE,
        related_name="evaluations",
    )

    attempt_number = models.PositiveIntegerField()

    passed = models.BooleanField()

    evaluation = models.JSONField()

    failed_checks = models.JSONField(default=list)

    regeneration_feedback = models.JSONField(default=list)
    changes_made = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["attempt_number"]

    def __str__(self):
        return (
            f"Run {self.lesson_run_id} "
            f"- Attempt {self.attempt_number}"
        )


class Memory(models.Model):
    failure_type = models.CharField(
        max_length=100,
        unique=True,
    )

    lesson_learned = models.TextField()

    occurrence_count = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-occurrence_count", "-updated_at"]

    def __str__(self):
        return (
            f"{self.failure_type} "
            f"({self.occurrence_count})"
        )