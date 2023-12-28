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

    def get_listified_posts_with_attributes(self, qs, get_parent_chain=False):
        """
        Get attributes of a list of posts passed in if elected for. Includes options:
        count of responses/threads to the current post and parents chain to original (root) topic post.
        """
        attr_obj_list = []
        for post_object in qs:
            attr_obj = [post_object]
            responses= post_object.responses()
            attr_obj.append(responses)
            # if getting the parent chain
            if get_parent_chain:
                parents_chain = post_object.get_parents_to_root_post()
                attr_obj.append(parents_chain)
            attr_obj_list.append(attr_obj)
        return attr_obj_list


    def get(self, request):
        """Base Get Functionality for a PostList class to be overridden."""
        template_name = ""
        context = {}
        return render(request, template_name, context)


class PostsListPage(PostListBase):
    """
    Return List of Posts (truncated) which are original topic posts only. Include links to Detailed posts,
    which display thread count.
    """
    def get(self, request):
        template_name = "posts/posts.html"
        context = {"utc_now": datetime.now(timezone.utc)}
        qs = Post.objects.all().topic_posts().published()
        if request.user.is_authenticated:
            my_qs = Post.objects.filter(user=request.user).topic_posts()
            qs = (qs | my_qs).distinct()

        # Append to new list with response/thread (children) counts of each
        posts_attributes = self.get_listified_posts_with_attributes(qs)
        # Add Pagination
        context['page_obj'] = self.paginate(posts_attributes, request)

        return render(request, template_name, context)


class PostDetailPage(PostListBase):
    """
    Retrieve a single post via a slug (detailed) and first level of response posts (truncated).
    Include links to responses to these posts with their thread counts. Main post's header shows links
     to parent posts all the way back to original topic post (collapsible if parent chain > 3).
    """
    def get(self, request, slug):
        obj = get_object_or_404(Post, slug=slug)
        template_name = "posts/detail-page.html"

        # gets a parent chain to root post (if applicable)
        [main_post_attributes] = self.get_listified_posts_with_attributes([obj],True)
        context = {"object": main_post_attributes}  # "card_parent_width_percent": 100}  # widest card will be the "parent" card of the page (the one most "original" to the response hierarchy) - might not be the OP if the OP is not on the page

        # Get whole discussion for post including drafts
        qs = obj.responses().published()
        if request.user.is_authenticated:
            my_qs = obj.responses().filter(user=request.user)
            qs = (qs | my_qs).distinct()

        # Add to new list with response posts/threads (i.e. children) counts of each response post
        response_posts_attributes = self.get_listified_posts_with_attributes(qs) # Todo: authentication on responses?
        # Add Pagination for responses
        context['page_obj'] = self.paginate(response_posts_attributes, request)

        return render(request, template_name, context)


# @login_required
@staff_member_required
def post_create_view(request, parent_slug=None):
    """ Create Post via a form. """
    template_name = "posts/post-form.html"
    # GET PARENT POST IF WRITING A RESPONSE
    if parent_slug:
        [parent_post] = Post.objects.all().filter(slug=parent_slug)
    else:
        parent_post = None
    context = {"title": "Create A New Post", "parent_post": parent_post}
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        if parent_post:
            obj.parent_post = parent_post
        #obj.title= form.cleaned_data.get("title") + "0"
        obj.save()
        #form = PostModelForm()  # If not redirecting but posting multiple in succession
        if parent_slug:
            return redirect("post_detail_page", parent_slug)
        else:
            return redirect("post_detail_page", obj.slug)
    context["form"] = form

    return render(request, template_name, context)


@staff_member_required
def post_update_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if obj.is_deleted:
        return redirect("post_detail_page", obj.slug)       # if already marked deleted just redirect to same deleted page to show it is deleted already
    # GET PARENT POST TO SHOW IF WRITING A RESPONSE
    if obj.parent_post:
            parent_post = obj.parent_post
    else:
        parent_post = None
    context = {"title": f"Update {obj.title}", "parent_post": parent_post}
    # GET EXISTING FORM
    form = PostModelForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        #return redirect(reverse("posts_index")) return redirect("post_detail_page", obj.slug)
        return redirect("post_detail_page",obj.slug )#args=form.fields.slug))
    template_name = "posts/post-form.html"
    context["form"] = form

    return render(request, template_name, context)


@staff_member_required
def post_delete_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    template_name = "posts/delete.html"
    if obj.is_deleted:
        # try:
        return redirect("post_detail_page", obj.slug)       # if already marked deleted just redirect to same deleted page to show it is deleted alreadys
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
        return redirect(reverse("posts_index"))
    context = {"object": obj}
    return render(request, template_name, context)
