from datetime import datetime, timezone
from django.shortcuts import render
from django.core.paginator import Paginator
from posts.models import Post
from posts.views import PostListBase
from .models import SearchQuery

class SearchView(PostListBase):
    """
    Displays the found posts matching a multi-filter search result (truncated).
    Include links to detailed view including response posts, with a thread count in the link.
    Post header shows links to parent posts all the way back to original topic post (collapsible if parent chain > 3).
    """
    def get(self, request):
        template_name = 'searches/view.html'

        # Assemble Query
        query = request.GET.get('q', None)
        user = None
        if request.user.is_authenticated:
            user=request.user
        context = {"query": query, "utc_now": datetime.now(timezone.utc)}

        # Save Query to DB
        if query is not None:
            SearchQuery.objects.create(user=user, query=query)

            # Run Search Query against DB for published, and for user if logged in
            posts_list = Post.objects.search_published(query=query)
            if request.user.is_authenticated:
                my_posts_list = Post.objects.search_user(user=user, query=query)
                posts_list = (posts_list|my_posts_list).distinct()

            context['results_count'] = posts_list.__len__()

            # Add to new list with threads (children) counts of each, and a parent chain to root post (if applicable)
            posts_attributes = self.get_listified_posts_with_attributes(posts_list, True)
            # Add Pagination
            context['page_obj'] = self.paginate(posts_attributes, request)

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