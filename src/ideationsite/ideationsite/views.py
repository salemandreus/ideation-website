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
    Main Page, also the redirected to page after login. Displays welcome text.
    If logged-in get latest updated posts (truncated). Include links to detailed view including response posts,
    with a thread count in the link.
    Post header shows links to parent posts all the way back to original topic post (collapsible if parent chain > 3).
    """
    def get(self, request):
        """Get the Welcome Page. If Logged in, get a list of most recent of all posts."""
        template_name = "../templates/index.html"
        if not request.user.is_authenticated:
            context = {"title": "Welcome!"}
        else:
            context = {
                        "title": "Welcome back, {username}!".format(username=request.user),
                        "utc_now": datetime.now(timezone.utc)
                       }

            def query_posts():
                qs = Post.objects.filter(user=request.user)[:8]
                return qs

            qs = query_posts()

            # Append list with posts, their thread counts and parent chain to root post
            posts_attributes = self.get_listified_posts_with_attributes(qs, True)
            # Add Pagination
            context['page_obj'] = self.paginate(posts_attributes, request)

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
