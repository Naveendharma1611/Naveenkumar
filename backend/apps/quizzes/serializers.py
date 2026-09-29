import copy

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Quiz, QuizAttempt, QuizQuestion


class QuizQuestionPublicSerializer(serializers.ModelSerializer):
    """Question as shown while taking a quiz: no answers or explanations."""

    type_label = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ["id", "type", "type_label", "prompt", "code", "code_language", "options", "points", "order"]


class QuizQuestionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = "__all__"

    def validate(self, attrs):
        candidate = QuizQuestion() if self.instance is None else copy.copy(self.instance)
        for key, value in attrs.items():
            setattr(candidate, key, value)
        try:
            candidate.clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict)
        return attrs


class QuizListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True, default=None)
    difficulty_label = serializers.CharField(source="get_difficulty_display", read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id", "slug", "title", "description", "category", "category_name", "difficulty", "difficulty_label",
            "time_limit_minutes", "show_leaderboard", "question_count", "is_published", "order",
        ]


class QuizDetailSerializer(QuizListSerializer):
    questions = QuizQuestionPublicSerializer(many=True, read_only=True)

    class Meta(QuizListSerializer.Meta):
        fields = QuizListSerializer.Meta.fields + ["questions"]


class QuizSubmitSerializer(serializers.Serializer):
    attempt_id = serializers.IntegerField(required=False, allow_null=True)
    answers = serializers.DictField(child=serializers.CharField(allow_blank=True, max_length=10000))


class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source="quiz.title", read_only=True)
    quiz_slug = serializers.CharField(source="quiz.slug", read_only=True)

    class Meta:
        model = QuizAttempt
        fields = [
            "id", "quiz", "quiz_title", "quiz_slug", "started_at", "submitted_at", "score", "max_score", "percent",
            "timed_out",
        ]
