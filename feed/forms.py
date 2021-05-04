from .models import Comment, Post
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        prepopulated_fields = {'slug': ('title')}
        fields = ['title', 'slug', 'img', 'content', 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commenter', 'body']
