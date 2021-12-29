from rest_framework import generics
from rest_framework import viewsets

from .models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleSerializer
from .permissions import IsAdminUserOrReadOnly


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_fields = ['author__username', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
