"""
URL configuration for ideationsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# from posts.views import (post_detail_page)

from . import views
from posts import views as posts_views


urlpatterns = [
    path("", views.index, name="index"),
    path("post/", posts_views.post_detail_page, name="post_detail_page"),
    path("about/", views.about, name="about"),
    path("story/", views.story, name="story"),
    path("contact/", views.contact, name="contact"),
    path("posts/", include("posts.urls")),
    path("admin/", admin.site.urls),
]