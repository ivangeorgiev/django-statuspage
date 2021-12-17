"""Test cases for djangostatuspage.config module."""

import pytest

from djangostatuspage import config
from djangostatuspage.admin import site

pytestmark = [pytest.mark.unit, pytest.mark.all]


@pytest.fixture
def djangostatuspage_settings(settings):
    """Get DJANGO_STATUSPAGE from project settings."""
    s = getattr(settings, "DJANGO_STATUSPAGE", {})
    setattr(settings, "DJANGO_STATUSPAGE", s)
    yield s


class TestAdminHeaders:
    """Test cases for admin site headers."""

    def test_admin_site_header_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_SITE_HEADER set from settings."""
        assert config.ADMIN_SITE_HEADER == djangostatuspage_settings["ADMIN_SITE_HEADER"]

    def test_admin_site_text_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_SITE_TITLE set from settings."""
        assert config.ADMIN_SITE_TITLE == djangostatuspage_settings["ADMIN_SITE_TITLE"]

    def test_admin_index_title_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_INDEX_TITLE set from settings."""
        assert config.ADMIN_INDEX_TITLE == djangostatuspage_settings["ADMIN_INDEX_TITLE"]

    def test_admin_site_header_set(self, djangostatuspage_settings):
        """Verify site.site_header set from settings."""
        assert site.site_header == djangostatuspage_settings["ADMIN_SITE_HEADER"]

    def test_admin_site_title_set(self, djangostatuspage_settings):
        """Verify site.site_title set from settings."""
        assert site.site_title == djangostatuspage_settings["ADMIN_SITE_TITLE"]

    def test_admin_index_title_set(self, djangostatuspage_settings):
        """Verify site.site_index_title set from settings."""
        assert site.index_title == djangostatuspage_settings["ADMIN_INDEX_TITLE"]
