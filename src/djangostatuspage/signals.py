"""Register receivers for Django signals."""

from django.db.models.signals import post_migrate

from . import services


def post_migrate_receiver(**kwargs):
    """Perform post migration actions."""
    services.ensure_system_user()
    services.ensure_default_status_page()


post_migrate.connect(post_migrate_receiver)
