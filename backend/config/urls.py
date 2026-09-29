import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import UserAdminViewSet
from apps.blog.views import BlogCategoryViewSet, BlogPostViewSet, TagViewSet
from apps.certificates.views import CertificateViewSet
from apps.contact.views import ContactMessageAdminViewSet, ContactSubmitView
from apps.core.views import AdminOverviewView, GlobalSearchView, HealthView
from apps.learning import views as learning
from apps.portfolio import views as portfolio
from apps.projects.views import ProjectViewSet, TechnologyViewSet
from apps.quizzes.views import MyAttemptsView, QuizQuestionViewSet, QuizViewSet

router = DefaultRouter()
router.register("skills", portfolio.SkillViewSet)
router.register("education", portfolio.EducationViewSet)
router.register("experience", portfolio.ExperienceViewSet)
router.register("achievements", portfolio.AchievementViewSet)
router.register("projects", ProjectViewSet)
router.register("technologies", TechnologyViewSet)
router.register("study/categories", learning.StudyCategoryViewSet)
router.register("study/courses", learning.CourseViewSet)
router.register("study/lessons", learning.LessonViewSet)
router.register("study/materials", learning.StudyMaterialViewSet)
router.register("interview/questions", learning.InterviewQuestionViewSet)
router.register("quizzes", QuizViewSet)
router.register("quiz-questions", QuizQuestionViewSet)
router.register("certificates", CertificateViewSet)
router.register("blog/posts", BlogPostViewSet)
router.register("blog/categories", BlogCategoryViewSet)
router.register("blog/tags", TagViewSet)
router.register("admin/users", UserAdminViewSet, basename="admin-users")
router.register("admin/messages", ContactMessageAdminViewSet, basename="admin-messages")

api_patterns = [
    path("auth/", include("apps.accounts.urls")),
    path("profile/", portfolio.SiteProfileView.as_view(), name="site-profile"),
    path("resume/", portfolio.ResumeView.as_view(), name="resume"),
    path("stats/", portfolio.StatsView.as_view(), name="stats"),
    path("study/lesson/<slug:category_slug>/<slug:lesson_slug>/", learning.LessonBySlugView.as_view(),
         name="lesson-by-slug"),
    path("study/progress/", learning.ProgressView.as_view(), name="progress"),
    path("study/bookmarks/", learning.BookmarkView.as_view(), name="bookmarks"),
    path("study/notes/", learning.LessonNoteView.as_view(), name="lesson-notes"),
    path("interview/categories/", learning.InterviewCategoriesView.as_view(), name="interview-categories"),
    path("student/dashboard/", learning.StudentDashboardView.as_view(), name="student-dashboard"),
    path("student/quiz-attempts/", MyAttemptsView.as_view(), name="my-quiz-attempts"),
    path("contact/", ContactSubmitView.as_view(), name="contact"),
    path("search/", GlobalSearchView.as_view(), name="search"),
    path("admin/overview/", AdminOverviewView.as_view(), name="admin-overview"),
    path("health/", HealthView.as_view(), name="health"),
    path("", include(router.urls)),
]

admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Content management"

urlpatterns = [
    path(os.getenv("ADMIN_URL", "django-admin/"), admin.site.urls),
    path("api/", include(api_patterns)),
    path("", include("apps.web.urls")),  # HTML pages
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
