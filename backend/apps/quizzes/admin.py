from django.contrib import admin

from apps.core.admin import PublishAdminMixin

from .models import Quiz, QuizAttempt, QuizQuestion


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 1
    fields = [
        ("type", "points", "order"), "prompt", ("code", "code_language"), "options", "correct_option",
        "accepted_answers", "explanation",
    ]


@admin.register(Quiz)
class QuizAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["title", "category", "difficulty", "time_limit_minutes", "is_published"]
    list_editable = ["is_published"]
    list_filter = ["category", "difficulty", "is_published"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [QuizQuestionInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "quiz", "percent", "score", "max_score", "submitted_at", "timed_out"]
    list_filter = ["quiz", "timed_out"]
    search_fields = ["user__email"]
    readonly_fields = [f.name for f in QuizAttempt._meta.fields]
