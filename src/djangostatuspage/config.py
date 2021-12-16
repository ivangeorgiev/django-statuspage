"""Configuration settings for djangostatuspage plugin."""

from django.conf import settings

# Define templates for __str__ methods of models
STR_TEMPLATE_INCIDENT = "{incident.incident_id}. {incident.title} ({incident.origin} - {incident.id_at_origin})"
STR_TEMPLATE_INCIDENT_UPDATE = "{update.title}"
STR_TEMPLATE_SYSTEM = "{system.category.name} - {system.name} ({system.alias})"
STR_TEMPLATE_SYSTEM_CATEGORY = "{category.name}"

USER_MODEL = settings.AUTH_USER_MODEL
