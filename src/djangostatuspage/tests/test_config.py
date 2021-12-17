"""Test cases for djangostatuspage.config module."""

import pytest

from djangostatuspage import config
from djangostatuspage.admin import site

pytestmark = [pytest.mark.unit]


@pytest.fixture
def djangostatuspage_settings(settings):
    """Get DJANGO_STATUSPAGE from project settings."""
    s = getattr(settings, "DJANGO_STATUSPAGE", {})
    setattr(settings, "DJANGO_STATUSPAGE", s)
    yield s


class TestAdminHeaders:
    """Test cases for admin site headers."""

    @pytest.mark.unit
    def test_admin_site_header_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_SITE_HEADER set from settings."""
        assert config.ADMIN_SITE_HEADER == djangostatuspage_settings["ADMIN_SITE_HEADER"]

    @pytest.mark.unit
    def test_admin_site_text_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_SITE_TITLE set from settings."""
        assert config.ADMIN_SITE_TITLE == djangostatuspage_settings["ADMIN_SITE_TITLE"]

    @pytest.mark.unit
    def test_admin_index_title_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_INDEX_TITLE set from settings."""
        assert config.ADMIN_INDEX_TITLE == djangostatuspage_settings["ADMIN_INDEX_TITLE"]

    @pytest.mark.unit
    def test_admin_site_header_set(self, djangostatuspage_settings):
        """Verify site.site_header set from settings."""
        assert site.site_header == djangostatuspage_settings["ADMIN_SITE_HEADER"]

    @pytest.mark.unit
    def test_admin_site_title_set(self, djangostatuspage_settings):
        """Verify site.site_title set from settings."""
        assert site.site_title == djangostatuspage_settings["ADMIN_SITE_TITLE"]

    @pytest.mark.unit
    def test_admin_index_title_set(self, djangostatuspage_settings):
        """Verify site.site_index_title set from settings."""
        assert site.index_title == djangostatuspage_settings["ADMIN_INDEX_TITLE"]

    @pytest.mark.system
    def test_admin_headers_present_in_response(self, admin_client):
        """Verify admin headers are present in response."""
        title = config.ADMIN_INDEX_TITLE
        site_title = config.ADMIN_SITE_TITLE
        site_header = config.ADMIN_SITE_HEADER
        response = admin_client.get(f"/{config.ADMIN_URL}")
        content = response.content.decode()
        assert response.status_code == 200
        assert f"<h1>{title}</h1>" in content
        assert f">{site_header}</a>" in content
        assert f"<title>{title}|{site_title}</title>"


class TestAdminUrl:
    """Test cases for custom admin url."""

    @pytest.mark.unit
    def test_admin_url_config_set(self, djangostatuspage_settings):
        """Verify config.ADMIN_URL is set from settings."""
        assert config.ADMIN_URL == djangostatuspage_settings["ADMIN_URL"]

    @pytest.mark.system
    def test_admin_opens_at_configured_url(self, admin_client):
        """Verify admin interface opens at url configured in ADMIN_URL."""
        response = admin_client.get(f"/{config.ADMIN_URL}")
        assert response.status_code == 200
