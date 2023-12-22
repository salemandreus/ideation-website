from django.urls import path

from posts.views import (
        PostDetailPage,
        post_update_view,
        post_delete_view,
        PostsListPage,
        post_create_view,
)

urlpatterns = [
    path("", PostsListPage.as_view(), name="posts_index"),
    path("<str:slug>/", PostDetailPage.as_view(), name="PostDetailPage"),
    path("<str:slug>/edit/", post_update_view, name="post_update_view"),
    path("<str:slug>/delete/", post_delete_view, name="post_delete_view"),
    path("<str:parent_slug>/post-new/", post_create_view, name="post_response_create_view"),
]