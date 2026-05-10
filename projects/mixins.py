from http import HTTPStatus

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404

from projects.constants import (
    RESPONSE_MSG_ACCESS,
    RESPONSE_MSG_METHOD,
    STATUS_ERROR,
)
from projects.models import Project


class ProjectOwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden(RESPONSE_MSG_ACCESS)


class ProjectActionMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.method != "POST":
            return JsonResponse(
                {"status": STATUS_ERROR, "message": RESPONSE_MSG_METHOD},
                status=HTTPStatus.METHOD_NOT_ALLOWED,
            )
        return super().dispatch(request, *args, **kwargs)

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs["pk"])
