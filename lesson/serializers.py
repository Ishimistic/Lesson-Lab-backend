from rest_framework import serializers


class LessonRequestSerializer(serializers.Serializer):
    topic = serializers.CharField(
        max_length=255,
        min_length=2,
        trim_whitespace=True,
    )