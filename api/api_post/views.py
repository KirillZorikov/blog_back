from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts.models import Follow, Group, Post
from . import serializers
from .filters import PostFilter
from .permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = PostFilter
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
    )
    def follow(self, request, *args, **kwargs):
        """Return all following's posts."""
        return self.list(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.annotate_like(self.request.user)
        if self.action == 'follow':
            return queryset.filter(author__following__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = None
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ('get', 'post')


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    http_method_names = ('get', 'post')

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
