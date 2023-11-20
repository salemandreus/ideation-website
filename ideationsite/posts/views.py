from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404

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


def posts_list_view(request):
    """" Return List of Posts. """
    # Todo : allow specify how many to show, then use this view in main page to show latest X posts
    qs = Post.objects.all()
    template_name = "posts/list.html"
    context = {"object_list": qs}
    return render(request, template_name, context)

# @login_required
@staff_member_required
def post_create_view(request):
    """ Create Post via a form. """
    # if not request.user.is_authenticated:     #Todo? if we implement users beyond the admin page
    #     return render(request, "not-a-user.html",{})
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        #obj.title= form.cleaned_data.get("title") + "0"
        obj.save()
        form = PostModelForm()
    template_name = "form.html"
    context = {"title": "Create A New Post", "form": form}

    return render(request, template_name, context)

def post_detail_view(request, slug):
    """Retrieve a single post via a slug"""

    obj = get_object_or_404(Post, slug=slug)  # Todo: reduce duplicate slugs include author name in slug??
    template_name = "posts/detail.html"
    context = {"object": obj}
    return render(request, template_name, context)

def post_update_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)  # Todo: reduce duplicate slugs include author name in slug??
    template_name = "blog/update.html"
    context = {"object": obj,"form": None}
    return render(request, template_name, context)

def post_delete_view(request, slug):
    obj = get_object_or_404(Post, slug=slug)  # Todo: reduce duplicate slugs include author name in slug??
    template_name = "posts/delete.html"
    context = {"object": obj}
    return render(request, template_name, context)

