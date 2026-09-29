from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminRole

SEARCH_LIMIT = 6


class GlobalSearchView(APIView):
    """Searches published content across the site. Returns results grouped by type with frontend URLs."""

    def get(self, request):
        from apps.blog.models import BlogPost
        from apps.certificates.models import Certificate
        from apps.learning.models import Course, InterviewQuestion, Lesson
        from apps.projects.models import Project

        q = request.query_params.get("q", "").strip()[:100]
        if len(q) < 2:
            return Response({"query": q, "groups": []})

        groups = []

        def add(key, label, items):
            if items:
                groups.append({"type": key, "label": label, "results": items})

        add("projects", "Projects", [
            {"title": p.title, "subtitle": p.summary, "url": f"/projects/{p.slug}"}
            for p in Project.objects.published()
            .filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(technologies__name__icontains=q))
            .distinct()[:SEARCH_LIMIT]
        ])
        add("courses", "Courses", [
            {"title": c.title, "subtitle": f"{c.category.name} · {c.get_level_display()}",
             "url": f"/study-materials/{c.category.slug}#{c.slug}"}
            for c in Course.objects.published().select_related("category")
            .filter(Q(title__icontains=q) | Q(description__icontains=q))[:SEARCH_LIMIT]
        ])
        add("lessons", "Lessons", [
            {"title": lesson.title, "subtitle": lesson.category.name,
             "url": f"/study-materials/{lesson.category.slug}/{lesson.slug}"}
            for lesson in Lesson.objects.published().filter(course__is_published=True).select_related("category")
            .filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))[:SEARCH_LIMIT]
        ])
        add("interview", "Interview Questions", [
            {"title": iq.question[:120], "subtitle": iq.category.name,
             "url": f"/interview/{iq.category.slug}?q={iq.id}"}
            for iq in InterviewQuestion.objects.published().select_related("category")
            .filter(Q(question__icontains=q) | Q(short_answer__icontains=q))[:SEARCH_LIMIT]
        ])
        add("blog", "Blog", [
            {"title": b.title, "subtitle": b.excerpt, "url": f"/blog/{b.slug}"}
            for b in BlogPost.objects.published()
            .filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))[:SEARCH_LIMIT]
        ])
        add("certificates", "Certificates", [
            {"title": c.name, "subtitle": c.provider, "url": f"/certificate/{c.credential_id}"}
            for c in Certificate.objects.published()
            .filter(Q(name__icontains=q) | Q(provider__icontains=q) | Q(skills__icontains=q))[:SEARCH_LIMIT]
        ])
        return Response({"query": q, "groups": groups})


class AdminOverviewView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        from apps.accounts.models import Role, User
        from apps.blog.models import BlogPost
        from apps.certificates.models import Certificate
        from apps.contact.models import ContactMessage
        from apps.learning.models import Course, InterviewQuestion, Lesson, StudyCategory
        from apps.projects.models import Project
        from apps.quizzes.models import Quiz, QuizAttempt

        def pair(qs):
            return {"total": qs.count(), "published": qs.filter(is_published=True).count()}

        return Response(
            {
                "users": {
                    "total": User.objects.count(),
                    "students": User.objects.filter(role=Role.STUDENT).count(),
                    "visitors": User.objects.filter(role=Role.VISITOR).count(),
                },
                "projects": pair(Project.objects),
                "study_categories": pair(StudyCategory.objects),
                "courses": pair(Course.objects),
                "lessons": pair(Lesson.objects),
                "interview_questions": pair(InterviewQuestion.objects),
                "quizzes": pair(Quiz.objects),
                "quiz_attempts": QuizAttempt.objects.exclude(submitted_at=None).count(),
                "certificates": pair(Certificate.objects),
                "blog_posts": pair(BlogPost.objects),
                "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
                "recent_users": list(
                    User.objects.order_by("-date_joined").values("id", "full_name", "email", "role", "date_joined")[:5]
                ),
            }
        )


class HealthView(APIView):
    authentication_classes = []

    def get(self, request):
        return Response({"status": "ok"})
