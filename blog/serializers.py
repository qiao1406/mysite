from rest_framework import serializers
from .models import Article, Category, Tag
from user_info.serializers import UserDescSerializer


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """在分类视图中文章的序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title'
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情页"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'created',
            'articles'
        ]


class TagSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserDescSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='blog:detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
            'created',
            'updated',
            'author'
        ]


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='name'
    )

    def validate_category_id(self, value):
        if value and not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value

    def to_internal_value(self, data):
        tags_names = data['tags']

        if isinstance(tags_names, list):
            for name in tags_names:
                if not Tag.objects.filter(name=name).exists():
                    Tag.objects.create(name=name)
        return super().to_internal_value(data)


class ArticleDetailSerializer(ArticleBaseSerializer):
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()  # 目录

    def get_body_html(self, obj):
        return obj.get_md()[0]
    
    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(ArticleBaseSerializer):

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}
