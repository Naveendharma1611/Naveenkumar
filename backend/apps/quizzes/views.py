from datetime import timedelta

from django.db.models import Count, Max, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.permissions import IsAdminOrReadOnly, IsStudentOrAdmin, is_admin
from apps.core.viewsets import PublishableViewSet

from .models import Quiz, QuizAttempt, QuizQuestion
from .serializers import (
    QuizAttemptSerializer,
    QuizDetailSerializer,
    QuizListSerializer,
    QuizQuestionAdminSerializer,
    QuizSubmitSerializer,
)

TIME_LIMIT_GRACE = timedelta(seconds=30)


class QuizViewSet(PublishableViewSet):
    queryset = Quiz.objects.select_related("category").annotate(question_count=Count("questions"))
    filterset_fields = {"category__slug": ["exact"], "difficulty": ["exact"]}
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        return QuizListSerializer if self.action == "list" else QuizDetailSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsStudentOrAdmin])
    def start(self, request, slug=None):
        quiz = self.get_object()
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)
        return Response(
            {"attempt_id": attempt.id, "started_at": attempt.started_at}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], permission_classes=[AllowAny])
    def submit(self, request, slug=None):
        """Grades answers. Scores are stored only for logged-in students who started an attempt."""
        quiz = self.get_object()
        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answers = serializer.validated_data["answers"]

        attempt = None
        attempt_id = serializer.validated_data.get("attempt_id")
        if attempt_id and request.user.is_authenticated:
            attempt = get_object_or_404(
                QuizAttempt, pk=attempt_id, user=request.user, quiz=quiz, submitted_at__isnull=True
            )

        results, score, max_score = [], 0, 0
        for question in quiz.questions.all():
            given = answers.get(str(question.id))
            verdict = question.grade(given)
            if question.is_auto_graded:
                max_score += question.points
                if verdict:
                    score += question.points
            results.append(
                {
                    "question_id": question.id,
                    "your_answer": given,
                    "correct": verdict,
                    "correct_option": question.correct_option,
                    "accepted_answers": question.accepted_answers,
                    "explanation": question.explanation,
                    "points": question.points,
                }
            )
        percent = round(score * 100 / max_score) if max_score else 0

        timed_out = False
        if attempt:
            now = timezone.now()
            if quiz.time_limit_minutes:
                timed_out = now - attempt.started_at > timedelta(minutes=quiz.time_limit_minutes) + TIME_LIMIT_GRACE
            attempt.answers = answers
            attempt.score, attempt.max_score, attempt.percent = score, max_score, percent
            attempt.submitted_at, attempt.timed_out = now, timed_out
            attempt.save()

        return Response(
            {
                "score": score,
                "max_score": max_score,
                "percent": percent,
                "saved": attempt is not None,
                "timed_out": timed_out,
                "results": results,
            }
        )

    @action(detail=True, methods=["get"])
    def leaderboard(self, request, slug=None):
        quiz = self.get_object()
        if not quiz.show_leaderboard:
            return Response([])
        rows = (
            QuizAttempt.objects.filter(quiz=quiz, submitted_at__isnull=False, timed_out=False)
            .values("user__full_name")
            .annotate(best=Max("percent"))
            .order_by("-best")[:10]
        )
        # Show first names only to protect student privacy.
        return Response(
            [{"rank": i + 1, "name": r["user__full_name"].split(" ")[0], "percent": r["best"]} for i, r in enumerate(rows)]
        )


class QuizQuestionViewSet(viewsets.ModelViewSet):
    """Admin-only management of questions (includes answers)."""

    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionAdminSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["quiz", "type"]

    def get_queryset(self):
        return super().get_queryset() if is_admin(self.request.user) else QuizQuestion.objects.none()


class MyAttemptsView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsStudentOrAdmin]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user).filter(~Q(submitted_at=None)).select_related("quiz")
