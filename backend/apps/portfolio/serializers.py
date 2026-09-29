from rest_framework import serializers

from .models import Achievement, Education, Experience, SiteProfile, Skill


def split_csv(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def split_lines(value: str) -> list[str]:
    return [v.strip() for v in value.splitlines() if v.strip()]


class SiteProfileSerializer(serializers.ModelSerializer):
    hero_badges_list = serializers.SerializerMethodField()
    technical_interests_list = serializers.SerializerMethodField()
    current_learning_list = serializers.SerializerMethodField()

    class Meta:
        model = SiteProfile
        exclude = ["id", "created_at"]

    def get_hero_badges_list(self, obj):
        return split_csv(obj.hero_badges)

    def get_technical_interests_list(self, obj):
        return split_lines(obj.technical_interests)

    def get_current_learning_list(self, obj):
        return split_lines(obj.current_learning)


class SkillSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Skill
        fields = [
            "id", "name", "category", "category_label", "description", "proficiency_label",
            "proficiency_percent", "icon", "order", "is_featured", "is_published",
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ["created_at", "updated_at"]


class ExperienceSerializer(serializers.ModelSerializer):
    type_label = serializers.CharField(source="get_type_display", read_only=True)
    technologies_list = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        exclude = ["created_at", "updated_at"]

    def get_technologies_list(self, obj):
        return split_csv(obj.technologies)


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        exclude = ["created_at", "updated_at"]
