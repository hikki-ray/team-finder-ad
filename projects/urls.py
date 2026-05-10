from django.urls import path

from projects.views import (
    ProjectCompleteView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectEditView,
    ProjectFavoriteListView,
    ProjectListView,
    ProjectToggleFavoriteView,
    ProjectToggleParticipateView,
)

app_name = "projects"


urlpatterns = [
    path("<int:pk>/", ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ProjectEditView.as_view(), name="edit"),
    path("<int:pk>/complete/", ProjectCompleteView.as_view(), name="complete"),
    path("<int:pk>/toggle-favorite/", ProjectToggleFavoriteView.as_view(), name="toggle-favorite"),
    path(
        "<int:pk>/toggle-participate/",
        ProjectToggleParticipateView.as_view(),
        name="toggle-participate",
    ),
    path("list/", ProjectListView.as_view(), name="list"),
    path("favorites/", ProjectFavoriteListView.as_view(), name="favorites"),
    path("create-project/", ProjectCreateView.as_view(), name="create-project"),
]
