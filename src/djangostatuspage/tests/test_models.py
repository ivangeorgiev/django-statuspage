"""Test module for testing djangostatuspage.models module."""

import pytest

from djangostatuspage import config, models

pytestmark = pytest.mark.unit


@pytest.mark.django_db
class TestIncident:
    """Test cases for testing the Incident model."""

    def test_str(self):
        """Verify string correct string representation of the model."""
        config.STR_TEMPLATE_INCIDENT = '{incident.title} - 1234'
        incident = models.Incident(title='My Incident')
        assert str(incident) == 'My Incident - 1234'


@pytest.mark.django_db
class TestIncidentUpdate:
    """Test cases for testing the IncidentUpdate model."""

    def test_str(self):
        """Verify string correct string representation of the model."""
        config.STR_TEMPLATE_INCIDENT_UPDATE = '{update.title} - abcd'
        update = models.IncidentUpdate(title='UpDate')
        assert str(update) == 'UpDate - abcd'


@pytest.mark.django_db
class TestSystem:
    """Test cases for testing the System model."""

    def test_str(self):
        """Verify string correct string representation of the model."""
        config.STR_TEMPLATE_SYSTEM = '{system.name} - sys'
        system = models.System(name='Engine')
        assert str(system) == 'Engine - sys'


@pytest.mark.django_db
class TestSystemCategory:
    """Test cases for testing the SystemCategory model."""

    def test_str(self):
        """Verify string correct string representation of the model."""
        config.STR_TEMPLATE_SYSTEM_CATEGORY = '{category.name} - cat'
        category = models.SystemCategory(name='Core')
        assert str(category) == 'Core - cat'
