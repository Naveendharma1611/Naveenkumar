from rest_framework import serializers

from .models import Project, ProjectCodeSnippet, ProjectImage, ProjectVideo, Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ["id", "name", "slug"]


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ["id", "image", "caption", "alt_text", "order"]


class ProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectVideo
        fields = ["id", "title", "video", "url", "order"]


class ProjectCodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeSnippet
        fields = ["id", "title", "language", "code", "order"]


class ProjectListSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    category_label = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "slug", "title", "category", "category_label", "summary", "cover_image", "technologies",
            "github_url", "live_demo_url", "is_featured", "is_sample", "is_published", "created_at",
        ]


class ProjectDetailSerializer(ProjectListSerializer):
    technology_names = serializers.ListField(
        child=serializers.CharField(max_length=60), write_only=True, required=False
    )
    images = ProjectImageSerializer(many=True, read_only=True)
    videos = ProjectVideoSerializer(many=True, read_only=True)
    code_snippets = ProjectCodeSnippetSerializer(many=True, read_only=True)

    class Meta(ProjectListSerializer.Meta):
        fields = ProjectListSerializer.Meta.fields + [
            "technology_names", "problem_statement", "objective", "dataset", "architecture", "data_flow",
            "implementation", "algorithm", "model_training", "evaluation", "results", "future_improvements",
            "documentation", "documentation_pdf", "pipeline_steps", "model_3d", "demo_video_url", "order",
            "images", "videos", "code_snippets", "updated_at",
        ]

    def validate_pipeline_steps(self, value):
        if not isinstance(value, list) or not all(isinstance(s, str) for s in value):
            raise serializers.ValidationError("Must be a list of step names.")
        return value

    def _set_technologies(self, project, names):
        if names is None:
            return
        techs = [Technology.objects.get_or_create(name=n.strip())[0] for n in names if n.strip()]
        project.technologies.set(techs)

    def create(self, validated_data):
        names = validated_data.pop("technology_names", None)
        project = super().create(validated_data)
        self._set_technologies(project, names)
        return project

    def update(self, instance, validated_data):
        names = validated_data.pop("technology_names", None)
        project = super().update(instance, validated_data)
        self._set_technologies(project, names)
        return project
