import pytest
from djangostatuspage import models
from djangostatuspage import config

pytestmark = pytest.mark.unit

@pytest.mark.django_db
class TestIncident:

    def test_str(self):
        config.STR_TEMPLATE_INCIDENT = '{incident.title} - 1234'
        incident = models.Incident(title='My Incident')
        assert str(incident) == 'My Incident - 1234'
        
@pytest.mark.django_db
class TestIncidentUpdate:

    def test_str(self):
        config.STR_TEMPLATE_INCIDENT_UPDATE = '{update.title} - abcd'
        update = models.IncidentUpdate(title='UpDate')
        assert str(update) == 'UpDate - abcd'


@pytest.mark.django_db
class TestSystem:

    def test_str(self):
        config.STR_TEMPLATE_SYSTEM = '{system.name} - sys'
        system = models.System(name='Engine')
        assert str(system) == 'Engine - sys'


@pytest.mark.django_db
class TestSystemCategory:

    def test_str(self):
        config.STR_TEMPLATE_SYSTEM_CATEGORY = '{category.name} - cat'
        category = models.SystemCategory(name='Core')
        assert str(category) == 'Core - cat'





