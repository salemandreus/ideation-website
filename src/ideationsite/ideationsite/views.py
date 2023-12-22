from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.core.paginator import Paginator

from .forms import ContactForm
from posts.models import Post
from datetime import datetime, timezone

from posts.views import PostListBase

class WelcomePage(PostListBase):
    """
    Main Page, also the redirected to page after login
    Displays welcome text.
    If logged-in retrieve a list of latest updated posts (truncated). Include links to detailed,
    including response posts, with a thread count in the link.
    Post headers contain links to parent posts all the way back to original topic post
    if not the original topic post.
    """

    def get(self, request):

        template_name = "../templates/index.html"

        if not request.user.is_authenticated:
            context = {"title": "Welcome!"}
        else:
            context = {
                        "title": "Welcome back, {username}!".format(username=request.user),
                        "utc_now": datetime.now(timezone.utc)
                       }

            qs = Post.objects.all()[:8]

            # Add to new list with threads (children) counts of each and a parent chain to root post (if applicable)
            posts_and_threads_counts = self.get_listified_posts_with_attributes(qs, True, True)

            # Add Pagination
            context['page_obj'] = self.paginate(posts_and_threads_counts, request)

        return render(request, template_name, context)


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
