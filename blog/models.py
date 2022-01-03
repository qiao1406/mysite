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
    # 文章类别
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles',
        db_constraint=False
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
