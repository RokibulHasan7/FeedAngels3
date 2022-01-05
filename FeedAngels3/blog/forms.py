from django import forms


from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'imgage', 'slug', 'author', 'content', 'status']
