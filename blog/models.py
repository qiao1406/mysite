from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    # 作者
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    # 文章类别，一篇文章只能属于一个类别
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles',
        db_constraint=False
    )
    # 文章标签，一篇文章可以有很多个标签
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_md(self):
        md = Markdown(extensions=['markdown.extensions.extra',
                                  'markdown.extensions.codehilite',
                                  'markdown.extensions.toc', ])
        md_body = md.convert(self.body)
        return md_body, md.toc


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=False,
        related_name='comments'
    )
    body = models.TextField(max_length=1024)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
