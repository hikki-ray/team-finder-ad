from http import HTTPStatus

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse

from core.constants import STATUS_ERROR
from projects.constants import (
    RESPONSE_MSG_ACCESS,
    RESPONSE_MSG_METHOD,
    RESPONSE_MSG_NOT_FOUND,
)
from projects.models import Project


class ProjectOwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner == self.request.user

    def handle_no_permission(self):
        return JsonResponse(
            {"status": STATUS_ERROR, "message": RESPONSE_MSG_ACCESS},
            status=HTTPStatus.FORBIDDEN,
        )


class ProjectActionMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.method != "POST":
            return JsonResponse(
                {"status": STATUS_ERROR, "message": RESPONSE_MSG_METHOD},
                status=HTTPStatus.METHOD_NOT_ALLOWED,
            )
        self._project = Project.objects.filter(pk=self.kwargs["pk"]).first()
        if self._project is None:
            return JsonResponse(
                {"status": STATUS_ERROR, "message": RESPONSE_MSG_NOT_FOUND},
                status=HTTPStatus.NOT_FOUND,
            )
        return super().dispatch(request, *args, **kwargs)

    def get_project(self):
        return self._project
