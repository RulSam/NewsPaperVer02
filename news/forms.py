from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=5)
    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'title',
            'text',
        ]

        def clean(self):
            cleanData = super().clean()
            author = cleanData.post('author')
            postCategory = cleanData.post('postCategory')
            title = cleanData.post('title')
            text = cleanData.post('text')
            return cleanData
