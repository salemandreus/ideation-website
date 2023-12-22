from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime, timezone
from django.core.paginator import Paginator

from .forms import PostModelForm
from .models import Post

from django.views import View


class PostListBase(View):
    """Will be inherited and overridden by other views that list posts."""

    def paginate(self, post_list, request):
        """paginate a list of posts"""

        paginator = Paginator(post_list, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return page_obj


class PostsListPage(PostListBase):
    """
    Return List of Posts (truncated) which are original topic posts only. Include links to non-visible posts
    with a thread count.
    """

    def get(self, request):

        # qs = reversed(Post.objects.published())
        template_name = "posts/posts.html"
        context = {"utc_now": datetime.now(timezone.utc)}

        qs = Post.objects.all().topic_posts().published()
        if request.user.is_authenticated:
            my_qs = Post.objects.filter(user=request.user).topic_posts()
            qs = (qs | my_qs).distinct()

        # Append to new list with response/thread (children) counts of each
        posts_and_threads_counts = []
        for post_object in qs:
            posts_and_threads_counts.append([post_object, post_object.responses().count()])

        # Add Pagination
        context['page_obj'] = self.paginate(posts_and_threads_counts, request)

        return render(request, template_name, context)

# @login_required
@staff_member_required
def post_create_view(request, parent_slug=None):
    """ Create Post via a form. """
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        if parent_slug:
            parent_post = Post.objects.all().filter(slug=parent_slug)
            [obj.parent_post] = parent_post
        #obj.title= form.cleaned_data.get("title") + "0"
        obj.save()
        #form = PostModelForm()  # If not redirecting but posting multiple in succession

        if parent_slug:
            return redirect(PostDetailPage, parent_slug)
        else:
            return redirect(PostDetailPage, obj.slug)

    template_name = "posts/post-form.html"
    context = {"title": "Create A New Post", "form": form}

    return render(request, template_name, context)

class PostDetailPage(PostListBase):
    """
    Retrieve a single post via a slug (detailed) and show first level of response posts (truncated).
    Include links to non-visible posts with a thread count, and main post's header contains links to parent
    posts all the way back to original topic post if not the original topic post.
    """

    def get(self, request, slug):

        obj = get_object_or_404(Post, slug=slug)
        template_name = "posts/detail-page.html"
        # gets a parent chain to root post (if applicable)
        parents_chain = obj.get_parents_to_root_post()
        main_post_and_parents_chain = ([obj, parents_chain])
        context = {"object": main_post_and_parents_chain}  # "card_parent_width_percent": 100}  # widest card will be the "parent" card of the page (the one most "original" to the response hierarchy) - might not be the OP if the OP is not on the page

        # Get whole discussion for post including drafts
        qs = Post.objects.all().published().filter(parent_post=obj.pk)
        if request.user.is_authenticated:
            my_qs = Post.objects.filter(user=request.user, parent_post=obj.pk)
            qs = (qs | my_qs).distinct()

        # Add to new list with response posts/threads (i.e. children) counts of each response post
        posts_and_threads_counts = []   # Todo: authentication on responses?
        for post_object in qs:
            posts_and_threads_counts.append([post_object, post_object.responses().count()])

        # Add Pagination for responses
        context['page_obj'] = self.paginate(posts_and_threads_counts, request)

        return render(request, template_name, context)


@staff_member_required
def post_update_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if obj.is_deleted:
        return redirect(PostDetailPage, obj.slug)       # if already marked deleted just redirect to same deleted page to show it is deleted already
    form = PostModelForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        #return redirect(reverse(PostsListPage)) return redirect(PostDetailPage, obj.slug)
        return redirect(PostDetailPage,obj.slug )#args=form.fields.slug))
    template_name = "posts/post-form.html"
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def post_delete_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    template_name = "posts/delete.html"
    if obj.is_deleted:
        # try:
        return redirect(PostDetailPage, obj.slug)       # if already marked deleted just redirect to same deleted page to show it is deleted alreadys
        # except:
    elif request.method == "POST":      # Only delete the post's contents, and keep "[Deleted post]" if it has any child posts
    #children = Post.objects.filter(parent_post=obj.pk)
        #if children.count() > 0:
            # Since we can't delete the entire post if it has children just delete contents,
        obj.is_deleted = True
        obj.title = "[Deleted Post]"
        obj.slug = f"deleted-post-{str(obj.pk)}"
        obj.content = ""
        obj.image = None
        obj.save()
        # obj.delete()
        return redirect(reverse(PostsListPage))
    context = {"object": obj}
    return render(request, template_name, context)
