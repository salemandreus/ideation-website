from django import forms

from .models import Post

class PostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content']

    def clean_title(self, *args, **kwargs ):
        title = self.cleaned_data.get('title')
        qs = Post.objects.filter(title__iexact=title)   # Todo: use this for emails when signing up
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try another one.")
        return title
