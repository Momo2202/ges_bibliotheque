from django.urls import path

from apps.authors.views import AuthorDetailView, AuthorListCreateView

app_name = "authors"

urlpatterns = [
    path(
        "",
        AuthorListCreateView.as_view(),
        name="author-list-create",
    ),
    path(
        "<int:pk>/",
        AuthorDetailView.as_view(),
        name="author-detail",
    ),
]
