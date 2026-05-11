import re

from django import forms

from core.constants import GITHUB_URL_PATTERN, MSG_GITHUB_INVALID
from projects.constants import MSG_GITHUB_TAKEN
from projects.models import Project


class ProjectCreateEditForm(forms.ModelForm):
    github_url = forms.URLField(
        required=True,
        widget=forms.URLInput(attrs={"placeholder": "https://github.com/<user>/<repo>"}),
    )

    class Meta:
        model = Project
        fields = ("name", "description", "github_url")

    def clean_github_url(self):
        url = self.cleaned_data["github_url"].strip()

        if not re.match(GITHUB_URL_PATTERN, url):
            raise forms.ValidationError(MSG_GITHUB_INVALID)

        normalized = url.rstrip("/")
        if self._github_url_taken(normalized):
            raise forms.ValidationError(MSG_GITHUB_TAKEN)

        return normalized

    def _github_url_taken(self, url):
        queryset = Project.objects.filter(github_url=url)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        return queryset.exists()
