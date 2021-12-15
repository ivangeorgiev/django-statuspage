import enum
from django.db import models
from . import config
from . import shortcuts

class AlertSeverity(enum.Enum):
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFORMATIONAL = 'information'
    VERBOSE = 'verbose'

class IncidentOrigin(enum.Enum):
    MANUAL = 'manual'

    @classmethod
    def get_choices(cls):
        def _make_choice(e):
            e.name.lower()
        return [(c.value, c.name) for c in cls]


class BaseModel(models.Model):
    """ BaseModel adds information on creation and modification times of the object. """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Incident(BaseModel):
    incident_id = models.BigAutoField(primary_key=True)
    origin = models.CharField(max_length=32, blank=True, null=True, choices=IncidentOrigin.get_choices())
    id_at_origin = models.CharField(max_length=255, blank=True, null=True)
    technical_details = models.TextField(blank=True, null=True, default='')
    is_hidden = models.BooleanField(default=False)
    created_by = models.ForeignKey(config.USER_MODEL, null=True, on_delete=models.SET_NULL,
            related_name='incident_created_set'
    )
    updated_by = models.ForeignKey(config.USER_MODEL, null=True, on_delete=models.SET_NULL,
            related_name='incident_updated_set'
    )

    class Meta:
        pass

"""
This is going to be developed soon:

class IncidentUpdate(BaseModel):
    incident_update_id = models.BigAutoField(primary_key=True)
    incident = models.ForeignKey(Incident)

"""
