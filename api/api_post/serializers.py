from rest_framework import serializers

from .models import Comment, Follow, Group, Post, User, Tag, LikeDislike


class GroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'slug', 'title')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'slug', 'title')


class AuthorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name')


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', 'image', 'group', 'tags', 'author')
        extra_kwargs = {'author': {'required': False}}


class PostSerializer(serializers.ModelSerializer):
    author = AuthorPostSerializer(read_only=True)
    group = GroupPostSerializer(required=False)
    tags = TagSerializer(required=False, many=True)
    likes_count = serializers.IntegerField(source='votes.likes.count',
                                           read_only=True)
    dislikes_count = serializers.IntegerField(source='votes.dislikes.count',
                                              read_only=True)
    comments_count = serializers.IntegerField(source='comments.count',
                                              read_only=True)
    liked = serializers.BooleanField()
    disliked = serializers.BooleanField()

    class Meta:
        fields = '__all__'
        extra_kwargs = {'text_preview': {'read_only': True}}
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    likes_count = serializers.IntegerField(source='votes.likes.count',
                                           read_only=True)
    dislikes_count = serializers.IntegerField(source='votes.dislikes.count',
                                              read_only=True)
    liked = serializers.BooleanField(read_only=True)
    disliked = serializers.BooleanField(read_only=True)
    # children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        exclude = ('lft', 'rght', 'tree_id')
        extra_kwargs = {'post': {'required': False}}
        # since we have post_id in params
        model = Comment

    # def get_children(self, obj):
    #     children = self.context['children'].get(obj.id, [])
    #     serializer = CommentSerializer(children, many=True,
    #                                    context=self.context)
    #     return serializer.data


class GroupSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count',
                                           read_only=True)

    class Meta:
        fields = ('id', 'title', 'slug', 'description', 'posts_count')
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


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'



