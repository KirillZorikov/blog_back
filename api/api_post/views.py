from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, AllowAny)

from .mixins import LikeDislikeMixins
from .models import Follow, Group, Post, Tag, User, Comment
from . import serializers
from .filters import PostFilter
from .ordering import PostCustomOrdering
from .permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet,
                     LikeDislikeMixins):
    pagination_class = None
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.filter().annotate_like_dislike(self.request.user)

    def perform_create(self, serializer):
        parent_id = self.request.data.get('parent')
        parent_comment = get_object_or_404(
            Comment,
            pk=parent_id,
        ) if parent_id else None
        if parent_comment and parent_comment.level > 2:
            parent_comment = parent_comment.parent
        serializer.save(author=self.request.user,
                        post_id=self.kwargs['post_id'],
                        parent=parent_comment)

    # def get_serializer_context(self):
    #     """terrible implementation of pretty nesting comments."""
    #     context = super(CommentViewSet, self).get_serializer_context()
    #     trees = self.get_queryset()
    #     children_dict = defaultdict(list)
    #     for tree in trees:
    #         descendants = tree.get_descendants()
    #         for descendant in descendants:
    #             children_dict[descendant.parent.pk].append(descendant)
    #     context.update({'children': children_dict})
    #     return context


class PostViewSet(viewsets.ModelViewSet,
                  LikeDislikeMixins):
    filter_backends = (DjangoFilterBackend, PostCustomOrdering, SearchFilter)
    filter_class = PostFilter
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    search_fields = ('text', 'author__username')

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def follow(self, request, *args, **kwargs):
        """Return all following's posts."""
        return self.list(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.annotate_like_dislike(self.request.user)
        if self.action == 'follow':
            return queryset.filter(author__following__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers.PostCreateUpdateSerializer
        elif self.action in ['like', 'dislike']:
            return serializers.LikeDislikeSerializer
        return serializers.PostSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.PostSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, PostCustomOrdering)
    filter_class = PostFilter
    http_method_names = ('get',)

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return Post.objects.filter(
            author=author
        ).annotate_like_dislike(self.request.user)


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = None
    queryset = Group.objects.annotate(posts_count=Count('posts'))
    serializer_class = serializers.GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('posts_count', 'title')
    http_method_names = ('get', 'post')
    lookup_field = 'slug'


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ('get', 'post')
    lookup_field = 'slug'


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = serializers.FollowSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    lookup_field = 'author__username'

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
