"""Status page services."""

from . import config, models


def get_status_page() -> models.StatusPage:
    """Get default status page object."""
    page = models.StatusPage.objects.first()
    if page is None:
        raise models.DoesNotExistError("Status page does not exist.")
    return page


def get_system_user():
    """Get system user object."""
    return config.USER_MODEL.objects.get(username=config.SYSTEM_USERNAME)


def ensure_default_status_page():
    """Make sure default status page exists."""
    try:
        get_status_page()
    except models.DoesNotExistError:
        page = models.StatusPage.objects.create(
            title=config.STATUS_PAGE_DEFAULT_TITLE,
            description=config.STATUS_PAGE_DEFAULT_DESCRIPTION,
            created_by=get_system_user(),
        )
        page.save()


def ensure_system_user():
    """Make sure system user exists."""
    try:
        get_system_user()
    except models.DoesNotExistError:
        system_user = config.USER_MODEL.objects.create(username=config.SYSTEM_USERNAME)
        system_user.save()
