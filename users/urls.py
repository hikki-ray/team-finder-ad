from django.urls import path

from users.views import (
    PasswordUpdateView,
    ProfileEditView,
    SignInView,
    SignUpView,
    UserDetailView,
    UserListView,
    sign_out,
)

app_name = "users"


urlpatterns = [
    path("login/", SignInView.as_view(), name="login"),
    path("logout/", sign_out, name="logout"),
    path("register/", SignUpView.as_view(), name="register"),
    path("edit-profile/", ProfileEditView.as_view(), name="edit-profile"),
    path("change-password/", PasswordUpdateView.as_view(), name="change-password"),
    path("list/", UserListView.as_view(), name="list"),
    path("<int:pk>/", UserDetailView.as_view(), name="detail"),
]
