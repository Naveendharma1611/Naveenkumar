from rest_framework import viewsets

from apps.core.permissions import IsAdminOrReadOnly
from apps.core.viewsets import PublishableViewSet

from .models import BlogCategory, BlogPost, Tag
from .serializers import BlogCategorySerializer, BlogPostDetailSerializer, BlogPostListSerializer, TagSerializer


class BlogPostViewSet(PublishableViewSet):
    queryset = BlogPost.objects.select_related("category", "author").prefetch_related("tags")
    filterset_fields = {"category__slug": ["exact"], "tags__slug": ["exact"], "is_featured": ["exact"]}
    search_fields = ["title", "excerpt", "content", "tags__name"]
    ordering_fields = ["published_at", "title"]

    def get_serializer_class(self):
        return BlogPostListSerializer if self.action == "list" else BlogPostDetailSerializer

    def get_queryset(self):
        return super().get_queryset().distinct()


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    lookup_field = "slug"


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    lookup_field = "slug"
