from django.shortcuts import render

from posts.models import Post

from .models import SearchQuery
# Create your views here.
def search_view(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user=request.user
    context = {"query": query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        posts_list = Post.objects.search(query=query)
        context['posts_list'] = posts_list
    return render(request, 'searches/view.html', context)