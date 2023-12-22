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

from django.conf import settings

# from posts.views import (post_detail_page)

from searches.views import SearchView
from . import views

from posts.views import (
        post_create_view,
)


urlpatterns = [
    path("", views.WelcomePage.as_view(), name="WelcomePage"),
    path("post-new/", post_create_view, name="post_create_view"),
    path("post/", include("posts.urls")),
    path("search/", SearchView.as_view()),
    path("about/", views.about, name="about"),
    path("story/", views.story, name="story"),
    # path("contact/", views.contact, name="contact"),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    # test mode
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)