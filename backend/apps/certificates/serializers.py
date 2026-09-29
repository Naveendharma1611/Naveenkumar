from rest_framework import serializers

from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        exclude = ["created_at", "updated_at"]

    def get_skills_list(self, obj):
        return [s.strip() for s in obj.skills.split(",") if s.strip()]
