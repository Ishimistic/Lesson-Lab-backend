from django.urls import path

from .views import GenerateLessonView


urlpatterns = [
    path(
        "generate/",
        GenerateLessonView.as_view(),
        name="generate-lesson",
    ),
]