from rest_framework import serializers

from .models import Course, InterviewQuestion, Lesson, StudyCategory, StudyMaterial


class StudyMaterialSerializer(serializers.ModelSerializer):
    kind_label = serializers.CharField(source="get_kind_display", read_only=True)

    class Meta:
        model = StudyMaterial
        fields = [
            "id", "title", "kind", "kind_label", "course", "lesson", "file", "external_url", "description",
            "is_downloadable", "requires_login", "order",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        logged_in = bool(request and request.user.is_authenticated)
        if (instance.requires_login and not logged_in) or not instance.is_downloadable:
            data["file"] = None
        return data


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "slug", "summary", "estimated_minutes", "order", "is_published"]


class CourseSerializer(serializers.ModelSerializer):
    level_label = serializers.CharField(source="get_level_display", read_only=True)
    lessons = serializers.SerializerMethodField()
    materials = StudyMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "category", "title", "slug", "level", "level_label", "description", "cover_image", "order",
            "is_published", "lessons", "materials",
        ]

    def get_lessons(self, obj):
        # `visible_lessons` is prefetched by the view with the right publish filter.
        lessons = getattr(obj, "visible_lessons", None)
        if lessons is None:
            lessons = obj.lessons.published()
        return LessonListSerializer(lessons, many=True).data


class StudyCategorySerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(read_only=True, required=False)
    course_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = StudyCategory
        fields = ["id", "name", "slug", "description", "icon", "order", "is_published", "lesson_count", "course_count"]


class LessonDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)
    course_level = serializers.CharField(source="course.get_level_display", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    materials = StudyMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "course", "course_title", "course_level", "category_name", "category_slug", "title", "slug",
            "summary", "content", "video_url", "estimated_minutes", "order", "is_published", "materials",
            "created_at", "updated_at",
        ]
        read_only_fields = ["category_name", "category_slug"]


class InterviewQuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    difficulty_label = serializers.CharField(source="get_difficulty_display", read_only=True)

    class Meta:
        model = InterviewQuestion
        fields = [
            "id", "category", "category_name", "category_slug", "question", "short_answer", "detailed_answer",
            "example", "code", "code_language", "interview_tip", "difficulty", "difficulty_label", "order",
            "is_published",
        ]


class ProgressToggleSerializer(serializers.Serializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.published())
    completed = serializers.BooleanField(default=True)


class BookmarkToggleSerializer(serializers.Serializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.published())


class LessonNoteSerializer(serializers.Serializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.published())
    content = serializers.CharField(allow_blank=True, max_length=20000)
