from rest_framework import serializers

from blog.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["status", "edited_by"]

    def validate(self, attrs):
        for s in self.fields:
            if s not in attrs:
                raise serializers.ValidationError({s: f"{s} is required"})
        return attrs
