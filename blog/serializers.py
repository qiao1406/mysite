from rest_framework import serializers
from .models import Article
from user_info.serializers import UserDescSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'created',
            'updated',
            'author'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
