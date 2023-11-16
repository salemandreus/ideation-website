from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template


def index(request):
    """Main Page, also the redirected to page after login"""
    if request.user.is_authenticated:
        context = {"title": "Welcome back, {username}!".format(username=request.user),
                   "latest_posts": [1, 2, 3, 4, 5]}  # Todo: replace with links pulled from DB and their dates
    else:
        context = {"title": "Welcome!"}
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html",{"title":"About Us"})


def contact(request):
    return render(request, "contact.html",{"title":"Contact Us"})


def story(request):
    """A text file is imported and rendered into this view along with the template."""
    story_file = "story.txt"
    template_obj = get_template(story_file)
    context = {"story": template_obj}
    rendered_text = template_obj.render(context)

    return render(request, "story.html", {"title": "Our Story", "subtitle": "Read Our Story", "story": rendered_text})
