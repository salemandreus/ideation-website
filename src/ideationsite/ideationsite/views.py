from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.core.paginator import Paginator

from .forms import ContactForm
from posts.models import Post
from datetime import datetime, timezone


def index(request):
    """Main Page, also the redirected to page after login"""
    #qs = reversed(Post.objects.all()[5:])
    qs = Post.objects.all()[:8]
    if request.user.is_authenticated:
        context = {"title": "Welcome back, {username}!".format(username=request.user)}
    else:
        context = {"title": "Welcome!"}

    # Add to new list with threads (children) counts of each
    posts_and_threads_counts = []
    for post_object in qs:
        posts_and_threads_counts.append([post_object, post_object.responses().count()])

    # Add Pagination
    paginator = Paginator(posts_and_threads_counts, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context["page_obj"] = page_obj

    context["utc_now" ] = datetime.now(timezone.utc)
    return render(request, "../templates/index.html", context)


def about(request):
    """A text file is imported and rendered into this view along with the template."""
    about_file = "about.txt"
    template_obj = get_template(about_file)
    context = {"about": template_obj}
    rendered_text = template_obj.render(context)

    return render(request, "../templates/about.html", {"title": "About Us", "subtitle": "Our Mission and Goal", "about": rendered_text})


# def contact(request): <!--Todo: sending emails and email markdown rendering on back-end-->
#     print(request.POST)
#     form = ContactForm(request.POST or None)
#     if form.is_valid():
#         print(form.cleaned_data)
#         form = ContactForm()
#     context = {
#         "title": "Contact Us",
#         "form": form
#     }
#     return render(request, "../templates/email-form.html", context)


def story(request):
    """A text file is imported and rendered into this view along with the template."""
    story_file = "story.txt"
    template_obj = get_template(story_file)
    context = {"story": template_obj}
    rendered_text = template_obj.render(context)

    return render(request, "../templates/story.html", {"title": "Our Story", "subtitle": "Read Our Story", "story": rendered_text})
