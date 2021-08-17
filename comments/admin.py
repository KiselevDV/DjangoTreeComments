from django.contrib import admin

from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)

admin.site.site_header = 'Дерево комментариев'
admin.site.site_title = 'Административный сайт'
