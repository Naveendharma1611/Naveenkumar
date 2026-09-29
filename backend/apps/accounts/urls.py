from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/", views.RefreshView.as_view(), name="token-refresh"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.MeView.as_view(), name="me"),
    path("upgrade-to-student/", views.UpgradeToStudentView.as_view(), name="upgrade-to-student"),
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password"),
    path("password-reset/", views.PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset/confirm/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
]
