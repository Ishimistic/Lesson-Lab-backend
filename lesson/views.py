from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LessonRequestSerializer
from .services.workflow import run_lesson_workflow


class GenerateLessonView(APIView):

    def post(self, request):
        serializer = LessonRequestSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data["topic"]

        try:
            result = run_lesson_workflow(topic)

            response_status = (
                status.HTTP_200_OK
                if result["status"] == "passed"
                else status.HTTP_422_UNPROCESSABLE_ENTITY
            )

            return Response(
                result,
                status=response_status,
            )

        except Exception as exc:
            return Response(
                {
                    "status": "error",
                    "message": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )