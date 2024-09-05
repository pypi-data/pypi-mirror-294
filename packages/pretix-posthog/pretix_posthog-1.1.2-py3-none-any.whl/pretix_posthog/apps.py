from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_posthog"
    verbose_name = "PostHog"

    class PretixPluginMeta:
        name = gettext_lazy("PostHog")
        author = "Daniel Malik"
        description = gettext_lazy("PostHog Integration for Pretix")
        visible = True
        version = __version__
        category = "INTEGRATION"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA
