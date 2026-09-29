from apps.core.viewsets import PublishableViewSet

from .models import Certificate
from .serializers import CertificateSerializer


class CertificateViewSet(PublishableViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    lookup_field = "credential_id"
    lookup_value_regex = "[^/]+"
    search_fields = ["name", "provider", "skills"]
    filterset_fields = ["provider"]
    pagination_class = None
