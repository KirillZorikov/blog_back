from posts.models import Comment, Follow, Group, Post, User, Tag


def add_group(slug, title, description):
    return Group.objects.create(
        title=title,
        description=description,
        slug=slug
    )


def add_user(username):
    return User.objects.create(
        username=username
    )


def add_post(group, user, text, tag=None, img=None):
    post = Post.objects.create(
        group=group,
        author=user,
        text=text,
        image=img
    )
    post.tags.set([tag]) if tag else 0
    return post


def add_follow(author, user):
    return Follow.objects.create(
        author=author,
        user=user
    )


def add_comment(post, author, text):
    return Comment.objects.create(
        author=author,
        post=post,
        text=text
    )


def add_tag(slug, title):
    return Tag.objects.create(
        title=title,
        slug=slug
    )
