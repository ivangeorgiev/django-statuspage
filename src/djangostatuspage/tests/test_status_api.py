"""Test cases for client API."""

import pytest

from djangostatuspage import models, services

pytestmark = [pytest.mark.all, pytest.mark.unit]


@pytest.mark.django_db
class TestStatusApi:
    """Test cases for status API endpoint."""

    def test_endpoint_exists_and_returns_result(self, client):
        """Verify that endpoint returns success."""
        response = client.get("/api/status/")
        assert response.status_code == 200

    def test_response_contains_page_details(self, client):
        """Verify that endpoint returns status page details."""
        sp = services.get_status_page()
        response = client.get("/api/status/").json()[0]
        assert sp.title == response["title"]
        assert sp.description == response["description"]

    def test_response_contains_categories(self, client):
        """Verify that endpoint returns categories ordered by rank."""
        cat_1 = models.SystemCategory(name="core", description="core systems", rank=100)
        cat_2 = models.SystemCategory(name="query", description="query systems", rank=50)
        cat_1.save()
        cat_2.save()
        response = client.get("/api/status/").json()[0]
        assert response["categories"] == [
            {
                "id": cat_2.system_category_id,
                "name": "query",
                "description": "query systems",
                "is_visible": True,
                "systems": [],
            },
            {
                "id": cat_1.system_category_id,
                "name": "core",
                "description": "core systems",
                "is_visible": True,
                "systems": [],
            },
        ]
