from rest_framework.permissions import SAFE_METHODS, BasePermission


def is_admin(user) -> bool:
    return bool(user and user.is_authenticated and (user.is_superuser or getattr(user, "role", None) == "ADMIN"))


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return is_admin(request.user)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or is_admin(request.user)


class IsStudentOrAdmin(BasePermission):
    message = "This area is available to students only."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.role == "STUDENT" or is_admin(user)))
