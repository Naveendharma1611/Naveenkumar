from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAdminOrReadOnly, IsStudentOrAdmin, is_admin
from apps.core.viewsets import PublishableViewSet

from .models import Bookmark, Course, InterviewQuestion, Lesson, LessonNote, Progress, StudyCategory, StudyMaterial
from .serializers import (
    BookmarkToggleSerializer,
    CourseSerializer,
    InterviewQuestionSerializer,
    LessonDetailSerializer,
    LessonListSerializer,
    LessonNoteSerializer,
    ProgressToggleSerializer,
    StudyCategorySerializer,
    StudyMaterialSerializer,
)


def lesson_filter(user) -> Q:
    return Q() if is_admin(user) else Q(is_published=True)


class StudyCategoryViewSet(PublishableViewSet):
    queryset = StudyCategory.objects.all()
    serializer_class = StudyCategorySerializer
    pagination_class = None
    search_fields = ["name", "description"]

    def get_queryset(self):
        published = Q(lessons__is_published=True, lessons__course__is_published=True)
        return (
            super()
            .get_queryset()
            .annotate(
                lesson_count=Count("lessons", filter=published, distinct=True),
                course_count=Count("courses", filter=Q(courses__is_published=True), distinct=True),
            )
        )

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        user = request.user
        lessons_qs = Lesson.objects.filter(lesson_filter(user)).order_by("order", "id")
        courses = (
            category.courses.filter(Q() if is_admin(user) else Q(is_published=True))
            .prefetch_related(Prefetch("lessons", queryset=lessons_qs, to_attr="visible_lessons"), "materials")
        )
        data = self.get_serializer(category).data
        data["courses"] = CourseSerializer(courses, many=True, context={"request": request}).data
        return Response(data)


class CourseViewSet(PublishableViewSet):
    queryset = Course.objects.select_related("category").prefetch_related("materials")
    serializer_class = CourseSerializer
    filterset_fields = {"category__slug": ["exact"], "level": ["exact"]}
    search_fields = ["title", "description"]


class LessonViewSet(viewsets.ModelViewSet):
    """Admin CRUD by id. Public lesson pages use LessonBySlugView."""

    queryset = Lesson.objects.select_related("course", "category").prefetch_related("materials")
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = {"course": ["exact"], "category__slug": ["exact"], "course__level": ["exact"]}
    search_fields = ["title", "summary", "content"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not is_admin(self.request.user):
            qs = qs.filter(is_published=True, course__is_published=True)
        return qs

    def get_serializer_class(self):
        return LessonListSerializer if self.action == "list" else LessonDetailSerializer


class LessonBySlugView(APIView):
    def get(self, request, category_slug, lesson_slug):
        user = request.user
        base = Lesson.objects.select_related("course", "category").prefetch_related("materials")
        if not is_admin(user):
            base = base.filter(is_published=True, course__is_published=True, category__is_published=True)
        lesson = get_object_or_404(base, category__slug=category_slug, slug=lesson_slug)

        siblings = list(
            Lesson.objects.filter(lesson_filter(user), course=lesson.course)
            .order_by("order", "id")
            .values("id", "title", "slug")
        )
        index = next(i for i, s in enumerate(siblings) if s["id"] == lesson.id)
        data = LessonDetailSerializer(lesson, context={"request": request}).data
        data["previous"] = siblings[index - 1] if index > 0 else None
        data["next"] = siblings[index + 1] if index < len(siblings) - 1 else None
        data["course_lessons"] = siblings
        data["user_state"] = None
        if user.is_authenticated:
            note = LessonNote.objects.filter(user=user, lesson=lesson).first()
            data["user_state"] = {
                "completed": Progress.objects.filter(user=user, lesson=lesson).exists(),
                "bookmarked": Bookmark.objects.filter(user=user, lesson=lesson).exists(),
                "note": note.content if note else "",
            }
        return Response(data)


class StudyMaterialViewSet(viewsets.ModelViewSet):
    queryset = StudyMaterial.objects.select_related("course", "lesson")
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["course", "lesson", "kind"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not is_admin(self.request.user):
            qs = qs.filter(Q(course__is_published=True) | Q(lesson__is_published=True))
        return qs


class InterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = InterviewQuestion.objects.select_related("category")
    serializer_class = InterviewQuestionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = {"category__slug": ["exact"], "difficulty": ["exact"]}
    search_fields = ["question", "short_answer", "detailed_answer"]

    def get_queryset(self):
        qs = super().get_queryset()
        if not is_admin(self.request.user):
            qs = qs.filter(is_published=True)
        return qs


class InterviewCategoriesView(generics.ListAPIView):
    serializer_class = StudyCategorySerializer
    pagination_class = None

    def get_queryset(self):
        return (
            StudyCategory.objects.filter(is_published=True)
            .annotate(lesson_count=Count("interview_questions", filter=Q(interview_questions__is_published=True)))
            .filter(lesson_count__gt=0)
        )

    def list(self, request, *args, **kwargs):
        data = self.get_serializer(self.get_queryset(), many=True).data
        for item in data:
            item["question_count"] = item.pop("lesson_count")
            item.pop("course_count", None)
        return Response(data)


class ProgressView(APIView):
    permission_classes = [IsStudentOrAdmin]

    def post(self, request):
        serializer = ProgressToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = serializer.validated_data["lesson"]
        if serializer.validated_data["completed"]:
            Progress.objects.get_or_create(user=request.user, lesson=lesson)
        else:
            Progress.objects.filter(user=request.user, lesson=lesson).delete()
        return Response({"lesson": lesson.id, "completed": serializer.validated_data["completed"]})


class BookmarkView(APIView):
    permission_classes = [IsStudentOrAdmin]

    def get(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user).select_related("lesson__category")
        return Response(
            [
                {
                    "id": b.id,
                    "lesson_id": b.lesson_id,
                    "title": b.lesson.title,
                    "slug": b.lesson.slug,
                    "category_slug": b.lesson.category.slug,
                    "category_name": b.lesson.category.name,
                    "created_at": b.created_at,
                }
                for b in bookmarks
            ]
        )

    def post(self, request):
        """Toggles the bookmark for a lesson."""
        serializer = BookmarkToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lesson = serializer.validated_data["lesson"]
        deleted, _ = Bookmark.objects.filter(user=request.user, lesson=lesson).delete()
        if not deleted:
            Bookmark.objects.create(user=request.user, lesson=lesson)
        return Response({"lesson": lesson.id, "bookmarked": not deleted}, status=status.HTTP_200_OK)


class LessonNoteView(APIView):
    permission_classes = [IsStudentOrAdmin]

    def put(self, request):
        serializer = LessonNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note, _ = LessonNote.objects.update_or_create(
            user=request.user,
            lesson=serializer.validated_data["lesson"],
            defaults={"content": serializer.validated_data["content"]},
        )
        return Response({"lesson": note.lesson_id, "content": note.content, "updated_at": note.updated_at})


class StudentDashboardView(APIView):
    permission_classes = [IsStudentOrAdmin]

    def get(self, request):
        from apps.quizzes.models import QuizAttempt

        user = request.user
        published = Q(lessons__is_published=True, lessons__course__is_published=True)
        categories = StudyCategory.objects.filter(is_published=True).annotate(
            total=Count("lessons", filter=published, distinct=True),
            done=Count("lessons", filter=published & Q(lessons__progress__user=user), distinct=True),
        )
        category_progress = [
            {
                "name": c.name,
                "slug": c.slug,
                "total": c.total,
                "completed": c.done,
                "percent": round(c.done * 100 / c.total) if c.total else 0,
            }
            for c in categories
            if c.total
        ]

        completed_courses = (
            Course.objects.filter(is_published=True)
            .annotate(
                total=Count("lessons", filter=Q(lessons__is_published=True), distinct=True),
                done=Count(
                    "lessons", filter=Q(lessons__is_published=True, lessons__progress__user=user), distinct=True
                ),
            )
            .filter(total__gt=0)
        )
        courses_completed = sum(1 for c in completed_courses if c.done == c.total)

        attempts = QuizAttempt.objects.filter(user=user, submitted_at__isnull=False).select_related("quiz")
        percents = [a.percent for a in attempts]
        recent_progress = Progress.objects.filter(user=user).select_related("lesson__category")[:5]
        recent_attempts = attempts.order_by("-submitted_at")[:5]

        activity = [
            {
                "type": "lesson",
                "title": f"Completed {p.lesson.title}",
                "link": f"/study-materials/{p.lesson.category.slug}/{p.lesson.slug}",
                "at": p.created_at,
            }
            for p in recent_progress
        ] + [
            {
                "type": "quiz",
                "title": f"Scored {a.percent}% on {a.quiz.title}",
                "link": f"/practice/{a.quiz.slug}",
                "at": a.submitted_at,
            }
            for a in recent_attempts
        ]
        activity.sort(key=lambda x: x["at"], reverse=True)

        return Response(
            {
                "name": user.full_name,
                "lessons_completed": Progress.objects.filter(user=user).count(),
                "courses_completed": courses_completed,
                "quiz_attempts": len(percents),
                "average_quiz_score": round(sum(percents) / len(percents)) if percents else None,
                "bookmarks": Bookmark.objects.filter(user=user).count(),
                "category_progress": category_progress,
                "recent_activity": activity[:8],
            }
        )
