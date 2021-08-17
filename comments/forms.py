from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма базового комментария - у которого нет 'родителя'"""

    class Meta:
        model = Comment
        fields = ('text',)
