"""Test cases for client API."""

import pytest

from djangostatuspage import models, services

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
STATUS_ENDPOINT_URL = "/api/status/"

pytestmark = [pytest.mark.all, pytest.mark.unit]


@pytest.fixture
def response(client, test_data):
    """Get status info from status API endpoint."""
    response = client.get(STATUS_ENDPOINT_URL).json()[0]
    return response


@pytest.fixture
def test_data():
    """Creat basic test data."""
    cat_1 = models.SystemCategory(name="core", description="core systems", rank=100)
    cat_2 = models.SystemCategory(name="query", description="query systems", rank=50)
    cat_1.save()
    cat_2.save()
    sys_1 = models.System(name="sys-1", description="sys-1-description", rank=100, category=cat_1)
    sys_2 = models.System(name="sys-2", description="sys-2-description", rank=20, category=cat_1)
    sys_1.save()
    sys_2.save()
    inc_1 = models.Incident(title="inc-1")
    upd_1 = models.IncidentUpdate(
        incident=inc_1,
        title="update-1",
        status="new",
        severity="critical",
        monitor_status="fired",
        affected_system=sys_1,
    )
    inc_1.save()
    upd_1.save()
    inc_2 = models.Incident(title="inc-2")
    upd_2 = models.IncidentUpdate(
        incident=inc_2,
        title="update-2",
        status="ack",
        severity="error",
        monitor_status="resolved",
        affected_system=sys_1,
    )
    inc_2.save()
    upd_2.save()
    inc_3 = models.Incident(title="inc-3")
    upd_3 = models.IncidentUpdate(
        incident=inc_3,
        title="update-3",
        status="ack",
        severity="information",
        monitor_status="fired",
        affected_system=sys_1,
    )
    inc_3.save()
    upd_3.save()
    ctx = {
        "cat_1": cat_1,
        "cat_2": cat_2,
        "sys_1": sys_1,
        "sys_2": sys_2,
        "inc_1": inc_1,
        "upd_1": upd_1,
        "inc_2": inc_2,
        "upd_2": upd_2,
        "inc_3": inc_3,
        "upd_3": upd_3,
    }
    print("TEST DATA ======================")
    return ctx


@pytest.mark.django_db
class TestStatusApi:
    """Test cases for status API endpoint."""

    def test_endpoint_exists_and_returns_result(self, client):
        """Verify that endpoint returns success."""
        response = client.get(STATUS_ENDPOINT_URL)
        assert response.status_code == 200

    def test_response_contains_page_details(self, response):
        """Verify that endpoint returns status page details."""
        sp = services.get_status_page()
        assert sp.title == response["title"]
        assert sp.description == response["description"]

    def test_response_contains_categories(self, response, test_data):
        """Verify that endpoint returns categories ordered by rank."""
        assert len(response["categories"]) == 2
        #
        actual_cat_1 = response["categories"][0]
        expect_cat_1 = test_data["cat_2"]
        assert actual_cat_1["id"] == expect_cat_1.system_category_id
        assert actual_cat_1["name"] == expect_cat_1.name
        assert actual_cat_1["description"] == expect_cat_1.description
        assert actual_cat_1["is_visible"] == expect_cat_1.is_visible
        #
        actual_cat_2 = response["categories"][1]
        expect_cat_2 = test_data["cat_1"]
        assert actual_cat_2["id"] == expect_cat_2.system_category_id
        assert actual_cat_2["name"] == expect_cat_2.name
        assert actual_cat_2["description"] == expect_cat_2.description
        assert actual_cat_2["is_visible"] == expect_cat_2.is_visible
        assert "systems" in actual_cat_2

    def test_response_contains_systems(self, response, test_data):
        """Verify that endpoint returns systems ordered by rank."""
        systems = response["categories"][1]["systems"]
        #
        assert len(systems) == 2
        #
        actual_sys_1 = systems[0]
        expect_sys_1 = test_data["sys_2"]
        assert actual_sys_1["id"] == expect_sys_1.system_id
        assert actual_sys_1["alias"] == expect_sys_1.alias
        assert actual_sys_1["name"] == expect_sys_1.name
        assert actual_sys_1["description"] == expect_sys_1.description
        assert actual_sys_1["is_visible"] == expect_sys_1.is_visible
        assert actual_sys_1["is_enabled"] == expect_sys_1.is_enabled
        assert "active_incidents" in actual_sys_1
        #
        actual_sys_2 = systems[1]
        expect_sys_2 = test_data["sys_1"]
        assert actual_sys_2["id"] == expect_sys_2.system_id
        assert actual_sys_2["alias"] == expect_sys_2.alias
        assert actual_sys_2["name"] == expect_sys_2.name
        assert actual_sys_2["description"] == expect_sys_2.description
        assert actual_sys_2["is_visible"] == expect_sys_2.is_visible
        assert actual_sys_2["is_enabled"] == expect_sys_2.is_enabled
        assert "active_incidents" in actual_sys_2

    def test_response_active_incidents_highest_severity(self, response):
        """Verify correctness of categories[*].systems[*].active_incidents.highest_severity."""
        assert response["categories"][1]["systems"][0]["active_incidents"]["highest_severity"] is None
        assert response["categories"][1]["systems"][0]["active_incidents"]["highest_severity"] == "critical"

    def test_response_active_incidents_results(self, response, test_data):
        """Verify correctness of categories[*].systems[*].active_incidents.results[*]."""
        actual_1 = response["categories"][1]["systems"][0]["active_incidents"]
        assert "results" in actual_1
        assert actual_1["results"] == []
        #
        actual_2 = response["categories"][1]["systems"][1]["active_incidents"]
        assert "results" in actual_2
        assert len(actual_2["results"]) == 3
        #
        result_1 = actual_2["results"][0]
        upd_1 = test_data["upd_1"]
        assert result_1["id"] == upd_1.incident_id
        assert result_1["title"] == upd_1.title
        assert result_1["description"] == upd_1.description
        assert result_1["severity"] == upd_1.severity
        assert result_1["status"] == upd_1.status
        assert result_1["monitor_status"] == upd_1.monitor_status
        assert result_1["is_enabled"] == upd_1.is_enabled
        assert result_1["is_visible"] == upd_1.is_visible
        assert result_1["last_update"] == upd_1.updated_at.strftime(DATETIME_FORMAT)
        #
        result_2 = actual_2["results"][1]
        upd_2 = test_data["upd_2"]
        assert result_2["id"] == upd_2.incident_id

    def test_response_active_incidents_counts(self, response):
        """Verify correctness of categories[*].systems[*].active_incidents.counts[*]."""
        assert "counts" in response["categories"][1]["systems"][0]["active_incidents"]
        #
        counts_1 = response["categories"][1]["systems"][0]["active_incidents"]["counts"]
        assert counts_1 == {
            "severity": {"critical": 0, "error": 0, "warning": 0, "information": 0, "verbose": 0},
            "status": {"new": 0, "ack": 0, "closed": 0},
            "monitor_status": {"fired": 0, "resolved": 0},
        }
        #
        counts_2 = response["categories"][1]["systems"][1]["active_incidents"]["counts"]
        assert counts_2 == {
            "severity": {"critical": 1, "error": 1, "warning": 0, "information": 1, "verbose": 0},
            "status": {"new": 1, "ack": 2, "closed": 0},
            "monitor_status": {"fired": 2, "resolved": 1},
        }
