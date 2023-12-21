from django.shortcuts import render
from django.core.paginator import Paginator

from posts.models import Post

from .models import SearchQuery
# Create your views here.
def search_view(request):
    """
    Displays the found posts matching a multi-filter search result (truncated).
    Include links to detailed view including response posts, with a thread count in the link.
    Post headers contain links to parent posts all the way back to original topic post if not
    the original topic post.
    """

    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user=request.user
    context = {"query": query}

    posts_and_threads_counts = []
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        posts_list = Post.objects.search(query=query)

        # Add to new list with threads (children) counts of each, and a parent chain to root post (if applicable)
        for post_object in posts_list:
            responses_count = post_object.responses().count()
            parents_chain = post_object.get_parents_to_root_post()
            posts_and_threads_counts.append([post_object, responses_count, parents_chain])

        # Add Pagination
        paginator = Paginator(posts_and_threads_counts, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['results_count'] = posts_and_threads_counts.__len__()


    return render(request, 'searches/view.html', context)