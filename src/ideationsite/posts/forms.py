from django import forms

from .models import Post
                                    # Todo s for slugs on form:
class PostForm(forms.Form):     # Todo: treat all slugs in url as lowercase
    title = forms.CharField()   # todo: slugify needs to convert visually on form to lowercase
    slug = forms.SlugField() #todo: auto-populate with a slug of the title, if already in use append it with a number
    content = forms.CharField(widget=forms.Textarea)
    # publish_date = forms.DateTimeField(widget=datetime)  #(help_text="") # Todo: potentially add calendar and time (split?) widget

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post    #Todo: add note on form explaining how publish date works and can be blank
        fields = ['title', 'image', 'slug', 'publish_date', 'content']  # Todo calendar widget , status note of when it's scheduled for - now or future or how past applies depending what's specified relative to now


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
