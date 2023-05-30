from django import forms
from django.db import models
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder' : 'Que esta pasando?'}), required=True)

    class Meta:
        model = Post
        fields = ['content']