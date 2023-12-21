from django.shortcuts import render
from django.core.paginator import Paginator

from posts.models import Post

from .models import SearchQuery
# Create your views here.
def search_view(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user=request.user
    context = {"query": query}

    posts_and_threads_counts = []
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        posts_list = Post.objects.search(query=query)

        # Add to new list with threads (children) counts of each
        for post_object in posts_list:
            posts_and_threads_counts.append([post_object, post_object.responses().count()])

        # Add Pagination
        paginator = Paginator(posts_and_threads_counts, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['results_count'] = posts_and_threads_counts.__len__()


    return render(request, 'searches/view.html', context)