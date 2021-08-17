from django.urls import path

from .views import base_view, create_comment, create_child_comment

urlpatterns = [
    path('post-comments/', base_view, name='base'),
    path('create-comment/', create_comment, name='comment_create'),
    path('create-child-comment/', create_child_comment,
         name='comment_child_create'),
]
