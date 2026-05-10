from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from core.constants import PAGE_SIZE
from users.constants import (
    FILTER_FAVORITE_AUTHORS,
    FILTER_INTERESTED_USERS,
    FILTER_MY_PARTICIPANTS,
    FILTER_OPTIONS,
    FILTER_PARTICIPATING_AUTHORS,
)
from users.forms import (
    LoginForm,
    ProfileUpdateForm,
    RegistrationForm,
)
from users.models import User


class SignUpView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "users/register.html"

    def get_success_url(self):
        return reverse("projects:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, form.instance)
        return response


class SignInView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    next_page = "projects:list"


def sign_out(request):
    logout(request)
    return redirect("projects:list")


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/change_password.html"

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


class UserListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        queryset = User.objects.order_by("-date_joined").distinct()
        active_filter = self.request.GET.get("filter")

        if not self.request.user.is_authenticated or not active_filter:
            return queryset

        user = self.request.user

        if active_filter == FILTER_FAVORITE_AUTHORS:
            return (
                queryset.filter(owned_projects__interested_users=user)
                .exclude(pk=user.pk)
                .distinct()
            )

        if active_filter == FILTER_PARTICIPATING_AUTHORS:
            return (
                queryset.filter(owned_projects__participants=user).exclude(pk=user.pk).distinct()
            )

        if active_filter == FILTER_INTERESTED_USERS:
            return queryset.filter(favorites__owner=user).exclude(pk=user.pk).distinct()

        if active_filter == FILTER_MY_PARTICIPANTS:
            return (
                queryset.filter(participated_projects__owner=user).exclude(pk=user.pk).distinct()
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "filter_options": FILTER_OPTIONS,
                "active_filter": self.request.GET.get("filter", ""),
            }
        )
        return context


class UserDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return User.objects.prefetch_related("owned_projects__participants").get(
            pk=self.kwargs["pk"]
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/edit_profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})
