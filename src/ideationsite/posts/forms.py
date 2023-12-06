from django import forms

from .models import Post

class PostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'slug', 'content', 'publish_date']


    def clean_title(self, *args, **kwargs):
        instance=self.instance
        print(instance)
        title = self.cleaned_data.get('title')
        qs = Post.objects.filter(title__iexact=title)   # Todo: use this for emails when signing up
        if instance is not None:
            qs = qs.exclude(pk=instance.pk) #id=instance.id # exclude comparisons against itself
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try another one.")
        return title

    def clean_slug(self, *args, **kwargs):
        instance = self.instance
        print(instance)
        slug = self.cleaned_data.get('slug')
        qs = Post.objects.filter(slug__iexact=slug) # backwards compatibility in slugs with uppercase exist since Django allows them by default without our validator
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This slug has already been used. Please try another one.")
        return slug.lower()
