import logging
import secrets
from base64 import b64encode
from hashlib import sha384

import posthog
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.middleware import _merge_csp, _parse_csp, _render_csp
from pretix.base.models import Order
from pretix.base.signals import order_paid
from pretix.control.signals import nav_event_settings
from pretix.presale.signals import html_page_header, process_response

logger = logging.getLogger(__name__)


def generate_nonce(length=12):
    return secrets.token_urlsafe(length)


@receiver(nav_event_settings, dispatch_uid="posthog_nav_event_settings")
def navbar_event_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [
        {
            "label": _("PostHog"),
            "url": reverse(
                "plugins:pretix_posthog:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_posthog"
                      and url.url_name.startswith("settings"),
        }
    ]


@receiver(html_page_header, dispatch_uid="posthog_html_page_header")
def html_page_header_presale(sender, request, **kwargs):
    project_api_key = sender.settings.get("ph_project_api_key")
    client_api_host = sender.settings.get("ph_client_api_host")

    if not project_api_key:
        return
    # Generate a sha256 integrity hash for the script tag
    script_content = """
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init('%s',{api_host:'%s'})
""" % (project_api_key, client_api_host)
    integrity = 'sha384-' + b64encode(sha384(script_content.encode("utf-8")).digest()).decode('utf-8')
    return f"""
<script integrity="{integrity}">{script_content}</script>
        """


@receiver(process_response, dispatch_uid="posthog_process_response")
def process_response_presale_csp(sender, request, response, **kwargs):
    project_api_key = sender.settings.get("ph_project_api_key")
    if project_api_key:
        if "Content-Security-Policy" in response:
            headers = _parse_csp(response["Content-Security-Policy"])
        else:
            headers = {}

        _merge_csp(
            headers,
            {
                "script-src": [
                    "'self'",
                    "'unsafe-inline'",
                    "'unsafe-eval'",
                    "https://*.posthog.com",
                    "blob:",
                ],
                "style-src": [
                    "'self'",
                    "'unsafe-inline'",
                    "https://*.posthog.com",
                ],
                "img-src": [
                    "'self'",
                    "https://*.posthog.com",
                ],
                "connect-src": [
                    "'self'",
                    "https://*.posthog.com",
                ],
            },
        )

        if headers:
            response["Content-Security-Policy"] = _render_csp(headers)

    return response


@receiver(order_paid, dispatch_uid="posthog_order_paid")
def posthog_order_paid(sender, order: Order, **kwargs):
    api_key = sender.settings.get("ph_project_api_key")
    client_api_host = sender.settings.get("ph_client_api_host")
    if api_key and client_api_host:
        ph = posthog.Posthog(api_key, client_api_host)
        ph.capture(order.code, "order_paid", {
            "value": order.total,
            "email": order.email,
        })
