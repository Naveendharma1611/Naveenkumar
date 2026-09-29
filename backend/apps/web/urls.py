from pathlib import Path

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve

from . import views
from .forms import LoginForm

msg = "web/message.html"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("experience/", views.experience, name="experience"),
    path("resume/", views.resume, name="resume"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project"),
    path("certifications/", views.certifications, name="certifications"),
    path("certificate/<str:credential_id>/", views.certificate, name="certificate"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="post"),
    path("study-materials/", views.study_materials, name="study"),
    path("study-materials/<slug:category>/", views.study_category, name="study_category"),
    path("study-materials/<slug:category>/<slug:lesson>/", views.lesson, name="lesson"),
    path("interview/", views.interview, name="interview"),
    path("interview/<slug:category>/", views.interview_category, name="interview_category"),
    path("practice/", views.practice, name="practice"),
    path("practice/<slug:slug>/", views.quiz, name="quiz"),
    path("contact/", views.contact, name="contact"),
    path("search/", views.search, name="search"),
    path("study/<path:path>", serve, {"document_root": Path(__file__).parent / "study"}, name="study_file"),
    path("robots.txt", TemplateView.as_view(template_name="web/robots.txt", content_type="text/plain")),
    # Accounts (Django session auth)
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="web/form_page.html", authentication_form=LoginForm, redirect_authenticated_user=True,
        extra_context={"title": "Log in", "button": "Log in", "alt": ("New here?", "/register/", "Create an account"),
                       "forgot": True}), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("forgot-password/", auth_views.PasswordResetView.as_view(
        template_name="web/form_page.html", extra_context={"title": "Reset password", "button": "Send reset link"}),
        name="password_reset"),
    path("forgot-password/sent/", auth_views.PasswordResetDoneView.as_view(
        template_name=msg, extra_context={"title": "Check your email",
                                          "text": "If that email has an account, a reset link is on its way."}),
        name="password_reset_done"),
    path("reset-password/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="web/form_page.html", extra_context={"title": "Choose a new password", "button": "Save password"}),
        name="password_reset_confirm"),
    path("reset-password/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name=msg, extra_context={"title": "Password updated", "text": "You can now log in.",
                                          "link": ("/login/", "Log in")}),
        name="password_reset_complete"),
    path("account/", views.account, name="account"),
    path("student/", views.student, name="student"),
]
