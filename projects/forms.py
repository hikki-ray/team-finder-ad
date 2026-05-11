from django import forms

from core.utils import clean_github_url
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
        return clean_github_url(
            self.cleaned_data.get("github_url"),
            model=Project,
            instance_pk=self.instance.pk,
            error_msg=MSG_GITHUB_TAKEN
        )
