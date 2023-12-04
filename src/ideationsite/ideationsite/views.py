from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from posts.models import Post


def index(request):
    """Main Page, also the redirected to page after login"""
    #qs = reversed(Post.objects.all()[5:])
    qs = Post.objects.all()[:8]
    if request.user.is_authenticated:
        context = {"title": "Welcome back, {username}!".format(username=request.user)}
    else:
        context = {"title": "Welcome!"}
    context["latest_posts"] = qs
    return render(request, "../templates/index.html", context)


def about(request):
    return render(request, "../templates/about.html", {"title": "About Us"})


def contact(request):
    print(request.POST)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()
    context = {
        "title": "Contact Us",
        "form": form
    }
    return render(request, "e-mail-form.html", context)


def story(request):
    """A text file is imported and rendered into this view along with the template."""
    story_file = "story.txt"
    template_obj = get_template(story_file)
    context = {"story": template_obj}
    rendered_text = template_obj.render(context)

    return render(request, "../templates/story.html", {"title": "Our Story", "subtitle": "Read Our Story", "story": rendered_text})
