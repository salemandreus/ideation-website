from django.shortcuts import render
from django.core.paginator import Paginator

from posts.models import Post

from .models import SearchQuery

from posts.views import PostListBase


class SearchView(PostListBase):
    """
    Displays the found posts matching a multi-filter search result (truncated).
    Include links to detailed view including response posts, with a thread count in the link.
    Post header shows links to parent posts all the way back to original topic post (collapsible if parent chain > 3).
    """
    def get(self, request):
        template_name = 'searches/view.html'
        query = request.GET.get('q', None)
        user = None
        if request.user.is_authenticated:
            user=request.user
        context = {"query": query}

        if query is not None:
            SearchQuery.objects.create(user=user, query=query)
            posts_list = Post.objects.search(query=query)
            context['results_count'] = posts_list.__len__()

            # Add to new list with threads (children) counts of each, and a parent chain to root post (if applicable)
            posts_and_threads_counts = self.get_listified_posts_with_attributes(posts_list, True, True)
            # Add Pagination
            context['page_obj'] = self.paginate(posts_and_threads_counts, request)

            return render(request, template_name, context)


    # queryset = Post.objects.filter(slug=slug)
    # if queryset.count() == 0:
    #     raise Http404
    # else:
    #     obj = queryset.first()


# def posts_SearchView(request):
#     """" Return List of Posts. """
#
#     qs = Post.objects.filter(title__icontains='hello')
#     template_name = "posts_search_results.html"
#     context = {"object_list" : qs}
#     return render(request, template_name, context)

#and post.created != post.updated