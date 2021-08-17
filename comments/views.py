from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CommentForm
from .models import Post, Comment
from .utils import create_comments_tree


def base_view(request):
    """Главная страница"""
    # Все комментарии к статье id=1 (queryset)
    comments = Post.objects.first().comments.all()
    # Преобразовать их в список диктов (рекурсивно)
    result = create_comments_tree(comments)
    comment_form = CommentForm(request.POST or None)
    context = {
        'comments': result,
        'comment_form': comment_form
    }
    return render(request, 'comments/base.html', context)


def create_comment(request):
    """Создание/изменение базового комментария (без родителя)"""
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.text = comment_form.cleaned_data['text']
        new_comment.content_type = ContentType.objects.get(model='post')
        new_comment.object_id = 1  # данный пример содержит только одну статью
        new_comment.parent = None
        new_comment.is_child = False
        new_comment.save()
    return HttpResponseRedirect('/post-comments')


@transaction.atomic
def create_child_comment(request):
    """Создание/изменение дочернего комментария"""
    # Из base.js user: '{{ request.user.username }}'
    user_name = request.POST.get('user')
    current_id = request.POST.get('id')
    text = request.POST.get('text')
    user = User.objects.get(username=user_name)
    content_type = ContentType.objects.get(model='post')
    parent = Comment.objects.get(id=int(current_id))
    is_child = False if not parent else True

    Comment.objects.create(
        user=user, text=text, content_type=content_type, object_id=1,
        parent=parent, is_child=is_child
    )
    # Все комментарии к статье id=1
    comments_ = Post.objects.first().comments.all()
    # Преобразовать их в список диктов (рекурсивно)
    comments_list = create_comments_tree(comments_)
    context = {
        'comments': comments_list,
    }
    return render(request, 'comments/base.html', context)
