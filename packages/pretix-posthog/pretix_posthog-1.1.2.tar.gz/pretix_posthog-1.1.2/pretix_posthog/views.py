from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin


class PostHogSettingsForm(SettingsForm):
    ph_project_api_key = forms.CharField(
        label=_("PostHog Project API Key"),
        required=True,
        help_text=_(
            "You will find the Project API Key in the Project settings."
        ),
        max_length=47,
        min_length=47,
    )

    ph_client_api_host = forms.URLField(
        label=_("PostHog Client API Host"),
        required=True,
        help_text=_(
            "PostHog Client API Host"
        ),
        initial="https://eu.i.posthog.com",
    )


class SettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = PostHogSettingsForm
    template_name = "pretix_posthog/settings.html"
    permission = "can_change_event_settings"

    def get_success_url(self):
        return reverse(
            "plugins:pretix_posthog:settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
