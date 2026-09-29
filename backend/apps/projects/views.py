from rest_framework import viewsets

from apps.core.permissions import IsAdminOrReadOnly
from apps.core.viewsets import PublishableViewSet

from .models import Project, Technology
from .serializers import ProjectDetailSerializer, ProjectListSerializer, TechnologySerializer


class ProjectViewSet(PublishableViewSet):
    queryset = Project.objects.prefetch_related("technologies", "images", "videos", "code_snippets")
    filterset_fields = {"category": ["exact", "in"], "is_featured": ["exact"], "technologies__slug": ["exact"]}
    search_fields = ["title", "summary", "technologies__name"]
    ordering_fields = ["order", "created_at", "title"]

    def get_serializer_class(self):
        return ProjectListSerializer if self.action == "list" else ProjectDetailSerializer

    def get_queryset(self):
        return super().get_queryset().distinct()


class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "slug"
