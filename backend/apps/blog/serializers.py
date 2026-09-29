from rest_framework import serializers

from .models import BlogCategory, BlogPost, Tag


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class BlogPostListSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "slug", "title", "excerpt", "featured_image", "category", "tags", "published_at",
            "reading_minutes", "is_featured", "is_published",
        ]


class BlogPostDetailSerializer(BlogPostListSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=BlogCategory.objects.all(), write_only=True, required=False, allow_null=True
    )
    tag_names = serializers.ListField(child=serializers.CharField(max_length=50), write_only=True, required=False)
    author_name = serializers.CharField(source="author.full_name", read_only=True, default=None)

    class Meta(BlogPostListSerializer.Meta):
        fields = BlogPostListSerializer.Meta.fields + [
            "content", "category_id", "tag_names", "author_name", "created_at", "updated_at",
        ]

    def _set_tags(self, post, names):
        if names is not None:
            post.tags.set([Tag.objects.get_or_create(name=n.strip())[0] for n in names if n.strip()])

    def create(self, validated_data):
        names = validated_data.pop("tag_names", None)
        validated_data.setdefault("author", self.context["request"].user)
        post = super().create(validated_data)
        self._set_tags(post, names)
        return post

    def update(self, instance, validated_data):
        names = validated_data.pop("tag_names", None)
        post = super().update(instance, validated_data)
        self._set_tags(post, names)
        return post
