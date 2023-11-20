from django.urls import path

from posts.views import (
        post_detail_view,
        post_update_view,
        post_delete_view,
        posts_list_view,
)

urlpatterns = [
    path("", posts_list_view, name="index"),
    path("<str:slug>/", post_detail_view, name="post_detail_view"),
    path("<str:slug>/edit/", post_update_view, name="post_update_view"),
    path("<str:slug>/delete/", post_delete_view, name="post_delete_view"),
]