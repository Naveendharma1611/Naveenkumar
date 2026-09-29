from django.contrib import admin

from apps.core.admin import PublishAdminMixin

from .models import Bookmark, Course, InterviewQuestion, Lesson, LessonNote, Progress, StudyCategory, StudyMaterial


@admin.register(StudyCategory)
class StudyCategoryAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["name", "slug", "order", "is_published"]
    list_editable = ["order", "is_published"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


class LessonInline(admin.TabularInline):
    model = Lesson
    fields = ["title", "slug", "order", "is_published"]
    extra = 0
    show_change_link = True


class CourseMaterialInline(admin.TabularInline):
    model = StudyMaterial
    fk_name = "course"
    fields = ["title", "kind", "file", "external_url", "is_downloadable", "requires_login", "order"]
    extra = 0


@admin.register(Course)
class CourseAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["title", "category", "level", "order", "is_published"]
    list_editable = ["order", "is_published"]
    list_filter = ["category", "level", "is_published"]
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline, CourseMaterialInline]


class LessonMaterialInline(admin.TabularInline):
    model = StudyMaterial
    fk_name = "lesson"
    fields = ["title", "kind", "file", "external_url", "is_downloadable", "requires_login", "order"]
    extra = 1


@admin.register(Lesson)
class LessonAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["title", "course", "category", "order", "is_published", "updated_at"]
    list_editable = ["order", "is_published"]
    list_filter = ["category", "course__level", "is_published"]
    search_fields = ["title", "summary", "content"]
    list_select_related = ["course", "category"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonMaterialInline]
    fields = ["course", "title", "slug", "summary", "content", "video_url", "estimated_minutes", "order", "is_published"]


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ["title", "kind", "course", "lesson", "is_downloadable", "requires_login"]
    list_filter = ["kind", "is_downloadable", "requires_login"]
    search_fields = ["title"]


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(PublishAdminMixin, admin.ModelAdmin):
    list_display = ["short_question", "category", "difficulty", "order", "is_published"]
    list_editable = ["difficulty", "order", "is_published"]
    list_filter = ["category", "difficulty", "is_published"]
    search_fields = ["question", "short_answer"]

    @admin.display(description="Question")
    def short_question(self, obj):
        return str(obj)


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ["user", "lesson", "created_at"]
    list_select_related = ["user", "lesson"]
    search_fields = ["user__email", "lesson__title"]


admin.site.register(Bookmark)
admin.site.register(LessonNote)
