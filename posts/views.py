from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, PostForm
from api.api_post.models import Follow, Group, Post, User, Tag, Comment

POSTS_PER_PAGE = 10


def index(request):
    sort = request.GET.get('sort') or 'pub_date'
    if sort not in ['pub_date', 'comments', 'likes']:
        raise Http404
    post_list = Post.objects.select_related(
        'author',
        'group',
    )
    if sort == 'comments':
        post_list = post_list.annotate(
            count=Count(sort)
        ).order_by('-count', '-pub_date')
    elif sort == 'likes':
        post_list = post_list.annotate(
            count=Count('likes') - Count('dislikes')
        ).order_by('-count', '-pub_date')
    param = f'sort={sort}&' if sort != 'pub_date' else ''
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/index.html', {
        'page': page,
        'paginator': paginator,
        'sort': sort,
        'param': param,
    })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related(
        'author',
        'group'
    )
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/group.html', {
        'group': group,
        'page': page,
        'paginator': paginator,
    })


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/add_post.html', {
            'form': form,
        })
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    form.save_m2m()
    return redirect('index')


@login_required
def post_edit(request, username, post_id):
    if username != request.user.username:
        return redirect('post', username, post_id)
    post = get_object_or_404(
        Post,
        pk=post_id,
        author__username=username,
    )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if not form.is_valid():
        return render(request, 'posts/add_post.html', {
            'form': form,
            'post': post,
        })
    form.save()
    return redirect('post', username, post_id)


def post_view(request, username, post_id):
    author = get_object_or_404(
        User,
        username=username,
    )
    post = get_object_or_404(
        Post,
        pk=post_id,
        author=author,
    )
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'posts/post.html', {
        'post': post,
        'author': author,
        'form': form,
        'comments': comments,
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author,
    ).exists()
    post_list = author.posts.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'author': author,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        'misc/500.html',
        {'path': request.path},
        status=500
    )


@login_required
def add_comment(request, username, post_id, comment_id=None):
    post = get_object_or_404(
        Post,
        pk=post_id,
        author__username=username
    )
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/post.html', {
            'post': post,
            'form': form,
            'comments': comments,
            'parent_id': comment_id,
        })
    parent_comment = get_object_or_404(
        Comment,
        pk=comment_id,
    ) if comment_id else None
    if parent_comment and parent_comment.level > 2:
        parent_comment = parent_comment.parent
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.parent = parent_comment
    comment.save()
    return redirect('post', username, post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/follow.html', {
        'page': page,
        'paginator': paginator,
    })


@login_required
def profile_follow(request, username):
    if request.user.username == username:
        return redirect('profile', username)
    author = get_object_or_404(User, username=username)
    args = {'user': request.user, 'author': author}
    if not Follow.objects.filter(**args).exists():
        Follow.objects.create(**args)
    return redirect('profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow = get_object_or_404(
        Follow,
        user=request.user,
        author=author,
    )
    follow.delete()
    return redirect('profile', username)


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list = tag.posts.all()
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'posts/tag.html', {
        'tag': tag,
        'page': page,
        'paginator': paginator,
    })


@login_required
def like(request, post_id=None, comment_id=None):
    url = request.get_full_path()
    params = '?'
    for param in request.GET:
        params += f'{param}={request.GET[param]}&' if param != 'next' else ''
    if request.GET.get('next') == reverse('index'):
        cache.clear()
    redirect_to = request.GET.get('next') or reverse('index')
    post = get_object_or_404(
        Post,
        pk=post_id,
    ) if post_id else None
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
    ) if comment_id else None
    liked_obj = post or comment
    if 'dislike' in url:
        liked_obj.add_dislike(request.user)
    elif 'like' in url:
        liked_obj.add_like(request.user)
    return redirect(f'{redirect_to}{params[:-1]}')


def search_page(request):
    search = request.GET.get('search')
    post_list = Post.objects.filter(text__icontains=search)
    paginator = Paginator(post_list, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'search.html', {
        'page': page,
        'paginator': paginator,
        'param': f'search={search}&',
        'search': search,
    })


def post_delete(request, username, post_id):
    if request.user.username != username:
        raise Http404
    post = get_object_or_404(
        Post,
        pk=post_id,
        author__username=username
    )
    post.delete()
    return redirect('index')
