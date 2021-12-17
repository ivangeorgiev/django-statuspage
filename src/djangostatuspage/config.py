"""Configuration settings for djangostatuspage plugin."""

from django.conf import settings
from django.contrib import admin, auth

# Define templates for __str__ methods of models
STR_TEMPLATE_INCIDENT = "{incident.incident_id}. {incident.title} ({incident.origin} - {incident.id_at_origin})"
STR_TEMPLATE_INCIDENT_UPDATE = "{update.title}"
STR_TEMPLATE_SYSTEM = "{system.category.name} - {system.name} ({system.alias})"
STR_TEMPLATE_SYSTEM_CATEGORY = "{category.name}"
STR_TEMPLATE_STATUS_PAGE = "{status_page.title}"

ADMIN_URL = "sp-admin/"

ADMIN_SITE_HEADER = admin.site.site_header
ADMIN_SITE_TITLE = admin.site.site_title
ADMIN_INDEX_TITLE = admin.site.index_title

STATUS_PAGE_DEFAULT_TITLE = "Status page"
STATUS_PAGE_DEFAULT_DESCRIPTION = "Here you can find system status information."

SYSTEM_USERNAME = "djangostatuspage"

USER_MODEL = auth.get_user_model()

globals().update(getattr(settings, "DJANGO_STATUSPAGE", {}))
