from django.urls import path

from apps.members.views import (
    MemberDetailView,
    MemberListCreateView,
)

app_name = "members"

urlpatterns = [
    path(
        "",
        MemberListCreateView.as_view(),
        name="member-list-create",
    ),
    path(
        "<int:pk>/",
        MemberDetailView.as_view(),
        name="member-detail",
    ),
]
