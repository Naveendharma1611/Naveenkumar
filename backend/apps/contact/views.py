from rest_framework import mixins, serializers, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.core.permissions import IsAdminRole

from .models import ContactMessage

MIN_FILL_MS = 2500  # humans take longer than this to fill in the form


class ContactSubmitSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)  # honeypot
    elapsed_ms = serializers.IntegerField(required=False, write_only=True, min_value=0)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message", "website", "elapsed_ms"]

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Please write at least 10 characters.")
        return value.strip()


class ContactSubmitView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"

    def post(self, request):
        serializer = ContactSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        is_bot = bool(data.pop("website", "")) or data.pop("elapsed_ms", MIN_FILL_MS) < MIN_FILL_MS
        if not is_bot:
            forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
            ContactMessage.objects.create(
                **data,
                ip_address=(forwarded.split(",")[0].strip() or request.META.get("REMOTE_ADDR")) or None,
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:300],
            )
        # Bots get the same success response so they don't learn to adapt.
        return Response({"detail": "Thanks! Your message has been sent."}, status=status.HTTP_201_CREATED)


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "is_read", "created_at"]
        read_only_fields = ["name", "email", "subject", "message", "created_at"]


class ContactMessageAdminViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminRole]
    filterset_fields = ["is_read"]
    search_fields = ["name", "email", "subject", "message"]
