from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.certificates.models import Certificate
from apps.certificates.serializers import CertificateSerializer
from apps.core.permissions import IsAdminOrReadOnly, is_admin
from apps.learning.models import Lesson, StudyCategory
from apps.projects.models import Project
from apps.projects.serializers import ProjectListSerializer

from .models import Achievement, Education, Experience, SiteProfile, Skill
from .serializers import (
    AchievementSerializer,
    EducationSerializer,
    ExperienceSerializer,
    SiteProfileSerializer,
    SkillSerializer,
)


class SiteProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = SiteProfileSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return SiteProfile.load()


class AdminEditableViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        if not is_admin(self.request.user) and hasattr(qs.model, "is_published"):
            qs = qs.filter(is_published=True)
        return qs


class SkillViewSet(AdminEditableViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_fields = ["category", "is_featured"]
    search_fields = ["name", "description"]


class EducationViewSet(AdminEditableViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class ExperienceViewSet(AdminEditableViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filterset_fields = ["type"]


class AchievementViewSet(AdminEditableViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class ResumeView(APIView):
    """Everything the resume page needs in one request."""

    def get(self, request):
        ctx = {"request": request}
        skills = Skill.objects.filter(is_published=True)
        grouped: dict[str, dict] = {}
        for skill in skills:
            group = grouped.setdefault(skill.category, {"category": skill.get_category_display(), "skills": []})
            group["skills"].append(skill.name)
        projects = Project.objects.published().filter(is_featured=True).prefetch_related("technologies")[:6]
        return Response(
            {
                "profile": SiteProfileSerializer(SiteProfile.load(), context=ctx).data,
                "education": EducationSerializer(Education.objects.all(), many=True).data,
                "experience": ExperienceSerializer(Experience.objects.filter(is_published=True), many=True).data,
                "skills": list(grouped.values()),
                "projects": ProjectListSerializer(projects, many=True, context=ctx).data,
                "certificates": CertificateSerializer(
                    Certificate.objects.published()[:10], many=True, context=ctx
                ).data,
                "achievements": AchievementSerializer(Achievement.objects.all(), many=True).data,
            }
        )


class StatsView(APIView):
    """Counters for the About section. Counts only real, published content."""

    def get(self, request):
        return Response(
            {
                "projects": Project.objects.published().count(),
                "certifications": Certificate.objects.published().count(),
                "skills": Skill.objects.filter(is_published=True).count(),
                "study_materials": Lesson.objects.published().count(),
                "study_categories": StudyCategory.objects.filter(is_published=True).count(),
            }
        )
