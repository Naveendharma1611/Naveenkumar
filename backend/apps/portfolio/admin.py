from django.contrib import admin

from .models import Achievement, Education, Experience, SiteProfile, Skill


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("full_name", "headline", "tagline", "hero_badges", "photo")}),
        ("About", {"fields": ("short_bio", "about", "career_objective", "technical_interests",
                              "current_learning", "professional_goals")}),
        ("Contact & links", {"fields": ("email", "phone", "location", "linkedin_url", "github_url", "website_url")}),
        ("Resume", {"fields": ("resume_pdf",)}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "proficiency_label", "is_featured", "is_published", "order"]
    list_editable = ["proficiency_label", "is_featured", "is_published", "order"]
    list_filter = ["category", "is_featured", "is_published"]
    search_fields = ["name", "description"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "start_year", "end_year", "score", "order"]
    list_editable = ["order"]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["role", "organization", "type", "start_date", "end_date", "is_published"]
    list_filter = ["type", "is_published"]
    search_fields = ["role", "organization"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "order"]
