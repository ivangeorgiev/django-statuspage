"""Test cases for the services module."""

import pytest

from djangostatuspage import config, models, services

pytestmark = [pytest.mark.all]


@pytest.mark.django_db
class TestDefaultObjects:
    """Other model-related test cases."""

    @pytest.mark.system
    def test_system_user_exists(self):
        """Verify that system user has been created."""
        user = config.USER_MODEL.objects.get(username=config.SYSTEM_USERNAME)
        assert user is not None

    @pytest.mark.system
    def test_default_status_page_exists(self):
        """Verify that default status page has been created."""
        page = models.StatusPage.objects.first()
        assert page is not None
        assert page.title == config.STATUS_PAGE_DEFAULT_TITLE
        assert page.description == config.STATUS_PAGE_DEFAULT_DESCRIPTION
        assert page.created_by == services.get_system_user()


@pytest.mark.django_db
class TestGetStatusPage:
    """Test cases for get_satus_page function."""

    @pytest.mark.system
    def test_returns_status_page(self):
        """Verify that returns StatusPage if exists."""
        for p in models.StatusPage.objects.all():
            p.delete()
        models.StatusPage.objects.create(title="TEST PAGE", description="MORE INFO")
        page = services.get_status_page()
        assert page.title == "TEST PAGE"
        assert page.description == "MORE INFO"

    @pytest.mark.system
    def tests_raises_doesntexsiterror(self):
        """Verify that raises DoesnotExistError if does not exist."""
        for p in models.StatusPage.objects.all():
            p.delete()
        with pytest.raises(models.DoesNotExistError):
            services.get_status_page()


@pytest.mark.django_db
class TestGetSystemUser:
    """Test cases for get_system_user function."""

    @pytest.mark.system
    def tests_returns_system_user(self):
        """Verify that returns system user if exists."""
        for p in config.USER_MODEL.objects.filter(username=config.SYSTEM_USERNAME):
            p.delete()
        config.USER_MODEL.objects.create(username=config.SYSTEM_USERNAME)
        user = services.get_system_user()
        assert user.username == config.SYSTEM_USERNAME
