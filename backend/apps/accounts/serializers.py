from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Role, StudentProfile, User


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["phone", "institution", "course_of_study", "graduation_year", "bio", "interests"]


class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(required=False)
    is_admin = serializers.BooleanField(source="is_admin_role", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "is_admin", "avatar", "date_joined", "student_profile"]
        read_only_fields = ["id", "email", "role", "is_admin", "date_joined"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("student_profile", None)
        instance = super().update(instance, validated_data)
        if profile_data is not None:
            profile, _ = StudentProfile.objects.get_or_create(user=instance)
            for key, value in profile_data.items():
                setattr(profile, key, value)
            profile.save()
        return instance


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "is_active", "date_joined", "last_login"]
        read_only_fields = ["id", "email", "date_joined", "last_login"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)
    role = serializers.ChoiceField(choices=[Role.STUDENT, Role.VISITOR], default=Role.STUDENT)

    class Meta:
        model = User
        fields = ["email", "full_name", "role", "password", "password_confirm"]

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_full_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Please enter your full name.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": ["Passwords do not match."]})
        candidate = User(email=attrs["email"], full_name=attrs["full_name"])
        try:
            password_validation.validate_password(attrs["password"], candidate)
        except Exception as exc:
            raise serializers.ValidationError({"password": list(getattr(exc, "messages", [str(exc)]))})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if user.role == Role.STUDENT:
            StudentProfile.objects.create(user=user)
        return user


class RoleTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Adds role/name claims so the frontend can route without an extra request."""

    default_error_messages = {"no_active_account": "Invalid email or password."}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = "ADMIN" if user.is_admin_role else user.role
        token["name"] = user.full_name
        return token

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get(self.username_field, "").strip().lower()
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user, context=self.context).data
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        invalid = serializers.ValidationError("This reset link is invalid or has expired.")
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(attrs["uid"])))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise invalid
        if not default_token_generator.check_token(user, attrs["token"]):
            raise invalid
        try:
            password_validation.validate_password(attrs["new_password"], user)
        except Exception as exc:
            raise serializers.ValidationError({"new_password": list(getattr(exc, "messages", [str(exc)]))})
        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(trim_whitespace=False)
    new_password = serializers.CharField(trim_whitespace=False)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        try:
            password_validation.validate_password(attrs["new_password"], self.context["request"].user)
        except Exception as exc:
            raise serializers.ValidationError({"new_password": list(getattr(exc, "messages", [str(exc)]))})
        return attrs
