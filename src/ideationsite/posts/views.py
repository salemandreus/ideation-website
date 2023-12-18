from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from datetime import datetime, timezone

from .forms import PostModelForm
from .models import Post


    # queryset = Post.objects.filter(slug=slug)
    # if queryset.count() == 0:
    #     raise Http404
    # else:
    #     obj = queryset.first()


# def posts_search_view(request):
#     """" Return List of Posts. """
#
#     qs = Post.objects.filter(title__icontains='hello')
#     template_name = "posts_search_results.html"
#     context = {"object_list" : qs}
#     return render(request, template_name, context)

#and post.created != post.updated
def posts_list_view(request):
    """" Return List of Posts. """
    # qs = reversed(Post.objects.published())
    qs = Post.objects.all().topic_posts().published()
    if request.user.is_authenticated:
        my_qs = Post.objects.filter(user=request.user).topic_posts()
        qs = (qs | my_qs).distinct()

    # Add to new list with threads (children) counts of each
    posts_and_threads_counts = []
    for post_object in qs:
        post_and_threads_count = [post_object, Post.objects.filter(parent_post=post_object.pk).count()]
        posts_and_threads_counts.append(post_and_threads_count)

    template_name = "posts/list.html"
    context = {"object_list": posts_and_threads_counts, "utc_now": datetime.now(timezone.utc)}
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
            return redirect(post_detail_view, parent_slug)
        else:
            return redirect(post_detail_view, obj.slug)

    template_name = "posts/post-form.html"
    context = {"title": "Create A New Post", "form": form}

    return render(request, template_name, context)

def post_detail_view(request, slug):
    """Retrieve a single post via a slug"""

    obj = get_object_or_404(Post, slug=slug)
    template_name = "posts/detail-page.html"

    # Get whole discussion for post including drafts
    qs = Post.objects.all().published().filter(parent_post=obj.pk)
    if request.user.is_authenticated:
        my_qs = Post.objects.filter(user=request.user, parent_post=obj.pk)
        qs = (qs | my_qs).distinct()

                # parent        # responses
    context = {"object": obj, "object_list": qs, "card_parent_width_percent": 100}  # widest card will be the "parent" card of the page (the one most "original" to the response hierarchy) - might not be the OP if the OP is not on the page

    return render(request, template_name, context)

@staff_member_required
def post_update_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if obj.is_deleted:
        return redirect(post_detail_view, obj.slug)       # if already marked deleted just redirect to same deleted page to show it is deleted already
    form = PostModelForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        #return redirect(reverse(posts_list_view)) return redirect(post_detail_view, obj.slug)
        return redirect(post_detail_view,obj.slug )#args=form.fields.slug))
    template_name = "posts/post-form.html"
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def post_delete_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    template_name = "posts/delete.html"
    if obj.is_deleted:
        # try:
        return redirect(post_detail_view, obj.slug)       # if already marked deleted just redirect to same deleted page to show it is deleted alreadys
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
        return redirect(reverse(posts_list_view))
    context = {"object": obj}
    return render(request, template_name, context)
