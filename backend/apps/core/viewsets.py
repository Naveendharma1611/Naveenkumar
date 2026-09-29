from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly, is_admin


class PublishableViewSet(viewsets.ModelViewSet):
    """Public read access to published items; admins can read everything and write."""

    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        if is_admin(self.request.user):
            return qs
        return qs.filter(is_published=True)
