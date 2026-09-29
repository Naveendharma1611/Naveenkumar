from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import image_validators


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    STUDENT = "STUDENT", "Student"
    VISITOR = "VISITOR", "Visitor"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email is required.")
        user = self.model(email=self.normalize_email(email).lower(), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("is_staff", False)
        extra.setdefault("is_superuser", False)
        extra.setdefault("role", Role.VISITOR)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password=None, **extra):
        extra.update(is_staff=True, is_superuser=True, role=Role.ADMIN)
        return self._create_user(email, password, **extra)


class User(AbstractUser):
    """Email is the login identifier; `role` drives authorization across the site."""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VISITOR, db_index=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, validators=image_validators)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    @property
    def is_admin_role(self) -> bool:
        return self.is_superuser or self.role == Role.ADMIN

    def save(self, *args, **kwargs):
        # Admins need Django-admin access to manage content.
        if self.role == Role.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    phone = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    course_of_study = models.CharField(max_length=150, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True, max_length=1000)
    interests = models.CharField(max_length=300, blank=True, help_text="Comma separated")

    def __str__(self):
        return f"Profile of {self.user.email}"
