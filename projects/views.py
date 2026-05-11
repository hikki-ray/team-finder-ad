from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View

from core.constants import PAGE_SIZE, STATUS_ERROR, STATUS_OK
from projects.constants import (
    RESPONSE_MSG_ACCESS,
    RESPONSE_MSG_INACTIVE,
)
from projects.forms import ProjectCreateEditForm
from projects.mixins import ProjectActionMixin, ProjectOwnerOnlyMixin
from projects.models import Project, ProjectState


class BaseProjectListView(ListView):
    model = Project
    paginate_by = PAGE_SIZE
    context_object_name = "projects"

    def get_queryset(self):
        return (
            self.base_queryset()
            .select_related("owner")
            .prefetch_related("participants")
            .order_by("-created_at")
        )

    def base_queryset(self):
        return Project.objects.all()


class ProjectListView(BaseProjectListView):
    template_name = "projects/project_list.html"


class ProjectFavoriteListView(LoginRequiredMixin, BaseProjectListView):
    template_name = "projects/favorite_projects.html"

    def base_queryset(self):
        return self.request.user.favorites.all()


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.select_related("owner").prefetch_related("participants")


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateEditForm
    template_name = "projects/create-project.html"
    context_object_name = "project"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context


class ProjectEditView(LoginRequiredMixin, ProjectOwnerOnlyMixin, UpdateView):
    model = Project
    form_class = ProjectCreateEditForm
    template_name = "projects/create-project.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context


class ProjectCompleteView(LoginRequiredMixin, ProjectActionMixin, View):
    def post(self, request, *args, **kwargs):
        project = self.get_project()

        if project.owner != request.user:
            return JsonResponse(
                {"status": STATUS_ERROR, "message": RESPONSE_MSG_ACCESS},
                status=HTTPStatus.FORBIDDEN,
            )

        if project.status != ProjectState.ACTIVE:
            return JsonResponse(
                {"status": STATUS_ERROR, "message": RESPONSE_MSG_INACTIVE},
                status=HTTPStatus.BAD_REQUEST,
            )

        project.status = ProjectState.INACTIVE
        project.save(update_fields=["status"])

        return JsonResponse(
            {"status": STATUS_OK, "project_status": ProjectState.INACTIVE},
            status=HTTPStatus.OK,
        )


class ProjectToggleFavoriteView(LoginRequiredMixin, ProjectActionMixin, View):
    def post(self, request, *args, **kwargs):
        project = self.get_project()

        if request.user.favorites.filter(pk=project.pk).exists():
            request.user.favorites.remove(project)
            favorited = False
        else:
            request.user.favorites.add(project)
            favorited = True

        return JsonResponse(
            {"status": STATUS_OK, "favorited": favorited},
            status=HTTPStatus.OK,
        )


class ProjectToggleParticipateView(LoginRequiredMixin, ProjectActionMixin, View):
    def post(self, request, *args, **kwargs):
        project = self.get_project()

        if project.participants.filter(pk=request.user.pk).exists():
            project.participants.remove(request.user)
            is_member = False
        else:
            project.participants.add(request.user)
            is_member = True

        return JsonResponse(
            {"status": STATUS_OK, "participant": is_member},
            status=HTTPStatus.OK,
        )
