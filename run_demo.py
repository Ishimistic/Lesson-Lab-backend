import os
import django
import json


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

django.setup()


from lesson.services.workflow import (
    run_lesson_workflow,
)


result = run_lesson_workflow(
    topic="Introduction to RAG",
    inject_demo_error=True,
)


print("\n" + "=" * 80)
print("END-TO-END SELF-EVALUATING DEMO")
print("=" * 80)

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
    )
)