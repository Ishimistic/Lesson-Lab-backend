from django.contrib import admin

from .models import EvaluationLog, LessonRun, Memory


@admin.register(LessonRun)
class LessonRunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "topic",
        "status",
        "attempts",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = ("topic",)


@admin.register(EvaluationLog)
class EvaluationLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lesson_run",
        "attempt_number",
        "passed",
        "created_at",
    )

    list_filter = ("passed",)


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "failure_type",
        "occurrence_count",
        "updated_at",
    )

    search_fields = (
        "failure_type",
        "lesson_learned",
    )