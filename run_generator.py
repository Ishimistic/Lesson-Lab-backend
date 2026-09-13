import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from lesson.services.generator import generate_lesson


lesson = generate_lesson(
    topic="Introduction to RAG",
    memory_context="No previous lessons learned.",
)

print("\n" + "=" * 80)
print("GENERATED LESSON")
print("=" * 80)

print(lesson)