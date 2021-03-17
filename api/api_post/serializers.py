from rest_framework import serializers

from .models import Comment, Follow, Group, Post, User, Tag


class GroupFromPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('slug', 'title')


class TagFromPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('slug', 'title')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    group = GroupFromPostSerializer(required=False)
    tags = TagFromPostSerializer(required=False, many=True)
    likes_count = serializers.IntegerField(source='likes.count',
                                           read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Post

    def get_liked(self, obj):
        """Check current user liked post."""
        return obj.liked


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    children = serializers.SerializerMethodField(source='get_children',
                                                 read_only=True)

    class Meta:
        fields = ('id', 'post_id', 'author', 'text',
                  'created', 'parent', 'children')
        extra_kwargs = {'parent': {'required': True}}
        model = Comment

    def get_children(self, obj):
        children = self.context['children'].get(obj.id, [])
        serializer = CommentSerializer(children, many=True,
                                       context=self.context)
        return serializer.data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        extra_kwargs = {'slug': {'required': False},
                        'description': {'required': False}}
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    def validate(self, data):
        if data['author'] == data['user']:
            raise serializers.ValidationError('You can\'t subscribe '
                                              'on herself.')
        return data

    class Meta:
        exclude = ('id',)
        model = Follow
