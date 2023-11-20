from django.urls import path

from posts.views import (
        post_detail_view,
        post_update_view,
        post_delete_view,
        posts_list_view,
)

urlpatterns = [
    path("", posts_list_view),
    path("<str:slug>/", post_detail_view, name="post_detail_view"),
    path("<str:slug>/edit/", post_detail_view, name="post_update_view"),
    path("<str:slug>/delete/", post_detail_view, name="post_delete_view"),
]