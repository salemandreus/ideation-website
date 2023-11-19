from django.shortcuts import render

from .models import Post


def post_detail_page(request):

    obj = Post.objects.get(id=1)
    template_name='post_detail.html'
    context= {"object" : obj}
    return render(request, template_name, context)
