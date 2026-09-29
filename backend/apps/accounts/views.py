import logging

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.core.permissions import IsAdminRole

from .models import Role, StudentProfile, User
from .serializers import (
    AdminUserSerializer,
    ChangePasswordSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    RoleTokenObtainPairSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


def auth_payload(user, request) -> dict:
    refresh = RoleTokenObtainPairSerializer.get_token(user)
    return {
        "user": UserSerializer(user, context={"request": request}).data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class AuthThrottleMixin:
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


class RegisterView(AuthThrottleMixin, generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(auth_payload(user, request), status=status.HTTP_201_CREATED)


class LoginView(AuthThrottleMixin, TokenObtainPairView):
    serializer_class = RoleTokenObtainPairSerializer
    authentication_classes = []


class RefreshView(TokenRefreshView):
    authentication_classes = []


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            pass  # already invalid or expired: logging out still succeeds
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpgradeToStudentView(APIView):
    """Lets a visitor account opt in to the student learning features."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role == Role.VISITOR:
            user.role = Role.STUDENT
            user.save(update_fields=["role"])
            StudentProfile.objects.get_or_create(user=user)
        return Response(auth_payload(user, request))


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"{settings.FRONTEND_URL}/reset-password.html?uid={uid}&token={token}"
            try:
                send_mail(
                    "Reset your password",
                    f"Hi {user.full_name},\n\nUse this link to reset your password (valid for 2 hours):\n{link}\n\n"
                    "If you did not request this, you can ignore this email.",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
            except Exception:
                logger.exception("Failed to send password reset email")
        # Same response whether or not the account exists, so registered emails aren't leaked.
        return Response({"detail": "If an account exists for that email, a reset link has been sent."})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "password_reset"

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response({"detail": "Your password has been reset. You can now log in."})


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return Response({"detail": "Password updated."})


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminRole]
    filterset_fields = ["role", "is_active"]
    search_fields = ["email", "full_name"]
    ordering_fields = ["date_joined", "last_login", "full_name"]
    http_method_names = ["get", "patch", "delete", "head", "options"]
