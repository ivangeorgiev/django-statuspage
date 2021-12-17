"""Django applicaiton configuration module."""

from django.apps import AppConfig


class DjangostatuspageConfig(AppConfig):
    """Application configuration for djangostatuspage."""

    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Django Status Page"
    name = "djangostatuspage"

    def ready(self):
        """Perform application initialization post Django ready."""
        from . import signals  # noqa
