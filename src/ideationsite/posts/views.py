from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

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
    # Todo : allow specify how many to show, then use this view in main page to show latest X posts
    # qs = reversed(Post.objects.published())
    qs = Post.objects.all().published()
    if request.user.is_authenticated:
        my_qs = Post.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = "posts/list.html"
    context = {"object_list": qs}
    return render(request, template_name, context)

# @login_required
@staff_member_required
def post_create_view(request):
    """ Create Post via a form. """
    # if not request.user.is_authenticated:     #Todo? if we implement users beyond the admin page
    #     return render(request, "not-a-user.html",{})
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        #obj.title= form.cleaned_data.get("title") + "0"
        obj.save()
        #form = PostModelForm()  # If not redirecting but posting multiple in succession
        # return redirect(reverse(posts_list_view)) #or redirect to here # Todo: Add a validation that says posted successfully after post is sent
        return redirect(post_detail_view, obj.slug)
        #return redirect(reverse(post_detail_view, args=obj.slug)) # or here   # Todo: nicer, prettier form design (theme and visual aesthetics)
    template_name = "form.html"
    context = {"title": "Create A New Post", "form": form}

    return render(request, template_name, context)

def post_detail_view(request, slug):
    """Retrieve a single post via a slug"""

    obj = get_object_or_404(Post, slug=slug)  # Todo: reduce duplicate slugs include author name in slug??
    template_name = "posts/detail-page.html"
    context = {"object": obj}
    return render(request, template_name, context)

@staff_member_required
def post_update_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)  # Todo: reduce duplicate slugs include author name in slug or auto-generated slug??
    if obj.is_deleted:
        # try:
        return redirect(post_detail_view, obj.slug)       # if already marked deleted just redirect to same deleted page
    form = PostModelForm(request.POST or None, request.FILES or None, instance=obj) # todo: does the redirect mean I don't need to "else" this? what happens to this state?
    if form.is_valid():
        form.save()
        #return redirect(reverse(posts_list_view)) return redirect(post_detail_view, obj.slug)
        return redirect(post_detail_view,obj.slug )#args=form.fields.slug))
    template_name = "form.html"
    context = {"title": f"Update {obj.title}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def post_delete_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)  # Todo: reduce duplicate slugs include author name in slug??
    template_name = "posts/delete.html"
    if obj.is_deleted:
        # try:
        return redirect(post_detail_view, obj.slug)       # if already marked deleted just redirect to same deleted page
        # except:
    elif request.method == "POST":      # Only delete the post's contents, and keep "[Deleted post]" if it has any child posts
    #children = Post.objects.filter(parent_post=obj.pk)
        #if children.count() > 0:
            # Since we can't delete the entire post if it has children just delete contents,
        obj.is_deleted = True
        obj.title = "[Deleted Post]"                # todo s: IMPORTANT:
        obj.slug = f"deleted-post-{str(obj.pk)}"    # Todo: slug form validation: don't allow manually naming or renaming slugs with case-insensitive "deleted_*" regex pattern on forms - make this pattern a global config/env?
        obj.content = ""                            # Todo: Make no longer editable if deleted?
        obj.image = None
        obj.save()
        #else:
           # obj.delete()            # Todo: config: make it configurable whether deleting is allowed at all or only if no comments, or whether to hide/archive posts so only admins can actually delete, and display a certain message (in which case model should not allow any deleting)
        return redirect(reverse(posts_list_view))
    context = {"object": obj}
    return render(request, template_name, context)
