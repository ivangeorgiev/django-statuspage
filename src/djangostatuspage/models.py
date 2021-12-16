"""Models for djangostatuspage."""

import datetime
import enum

from django.db import models

from . import config, shortcuts

MAX_TIMESTAMP = datetime.datetime(3000, 1, 1).replace(tzinfo=datetime.timezone.utc)
"""Timestamp indicating open record for models with validity range (e.g. valid_from, valid_until)."""


class IncidentSeverity(enum.Enum):
    """Define possible values for incident severity."""

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFORMATIONAL = "information"
    VERBOSE = "verbose"


class IncidentOrigin(enum.Enum):
    """Define possible values for incident origin."""

    MANUAL = "manual"


class IncidentStatus(enum.Enum):
    """Define possible values for incident status."""

    NEW = "new"
    ACKNOWLEDGED = "ack"
    CLOSED = "closed"


class IncidentMonitorStatus(enum.Enum):
    """Define possible values for the monitor status of an incident."""

    FIRED = "fired"
    RESOLVED = "resolved"


class BaseModel(models.Model):
    """BaseModel adds information on creation and modification times of the object."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model meta."""

        abstract = True


class Incident(BaseModel):
    """Model to represent an incident."""

    incident_id = models.BigAutoField(primary_key=True)
    origin = models.CharField(max_length=32, blank=True, null=True, choices=shortcuts.get_enum_choices(IncidentOrigin))
    id_at_origin = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="incident_created_set"
    )
    updated_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="incident_updated_set"
    )

    def __str__(self):
        """Get string representation of the object."""
        return config.STR_TEMPLATE_INCIDENT.format(incident=self)


class IncidentUpdate(BaseModel):
    """Record a change to an incident (incident update)."""

    incident_update_id = models.BigAutoField(primary_key=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    technical_details = models.TextField(blank=True, null=True, default="")
    severity = models.TextField(max_length=32, choices=shortcuts.get_enum_choices(IncidentSeverity))
    status = models.CharField(max_length=32, choices=shortcuts.get_enum_choices(IncidentStatus))
    affected_system = models.ForeignKey("System", null=True, default=None, blank=True, on_delete=models.CASCADE)
    monitor_status = models.CharField(max_length=32, choices=shortcuts.get_enum_choices(IncidentMonitorStatus))
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    is_enabled = models.BooleanField(default=True, verbose_name="Enabled")
    effective_until = models.DateTimeField(default=MAX_TIMESTAMP)
    created_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="incident_update_created_set"
    )
    updated_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="incident_update_updated_set"
    )

    def __str__(self):
        """Get string representation of the object."""
        return config.STR_TEMPLATE_INCIDENT_UPDATE.format(update=self)


class System(BaseModel):
    """Define systems reflected on the status page."""

    system_id = models.BigAutoField(primary_key=True, verbose_name="id")
    alias = models.CharField(max_length=128, null=True)
    category = models.ForeignKey("SystemCategory", null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    is_enabled = models.BooleanField(default=True, verbose_name="Enabled")
    created_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="system_created_set"
    )
    updated_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="system_updated_set"
    )

    def __str__(self):
        """Get string representation of the object."""
        return config.STR_TEMPLATE_SYSTEM.format(system=self)


class SystemCategory(BaseModel):
    """Define a list of system categories."""

    system_category_id = models.BigAutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255)
    rank = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    created_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="system_category_created_set"
    )
    updated_by = models.ForeignKey(
        config.USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="system_category_updated_set"
    )

    def __str__(self):
        """Get string representation of the object."""
        return config.STR_TEMPLATE_SYSTEM_CATEGORY.format(category=self)

    class Meta:
        """Model meta."""

        verbose_name_plural = "system categories"
