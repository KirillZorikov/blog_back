from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import ClearableFileInput

from api.api_post.models import Comment, Post


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'django/forms/widgets/file.html'

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False,
                             widget=CustomClearableFileInput)
    #text = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['group'].empty_label = 'Выберите сообщество*'

    class Meta:
        model = Post
        fields = ['text', 'group', 'tags', 'image']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["text"]
