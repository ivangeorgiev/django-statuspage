"""Schemas module."""
from django.db.models import Count
from rest_framework import schemas, serializers

from djangostatuspage import shortcuts

from . import models

# TODO(ig): Implement open-api (https://github.com/ivangeorgiev/django-statuspage/issues/9)


class StatusPageMethodField(serializers.SerializerMethodField):
    """Abstract method field."""

    def __init__(self, many=False, method_name=None, **kwargs):
        """Create object instance."""
        super().__init__(**kwargs)
        self.many = many


class SystemCategoryMethodField(StatusPageMethodField):
    """System categories method field."""

    pass


class SystemMethodField(StatusPageMethodField):
    """Systems method field."""

    pass


class SystemIncidentSummaryMethodField(StatusPageMethodField):
    """System status method field."""

    pass


class IncidentCountsSerializer(serializers.Serializer):
    """Serializer for incident counts."""

    def to_representation(self, updates):
        """Get representation from updates QuerySet."""
        severity_counts = {e.value: 0 for e in models.IncidentSeverity}
        for s in updates.values("severity").annotate(count=Count("*")):
            severity_counts[s["severity"]] = s["count"]
        status_counts = {e.value: 0 for e in models.IncidentStatus}
        for s in updates.values("status").annotate(count=Count("*")):
            status_counts[s["status"]] = s["count"]
        monitor_counts = {e.value: 0 for e in models.IncidentMonitorStatus}
        for s in updates.values("monitor_status").annotate(count=Count("*")):
            monitor_counts[s["monitor_status"]] = s["count"]
        result = {
            "severity": severity_counts,
            "status": status_counts,
            "monitor_status": monitor_counts,
        }
        return result


class ActiveIncidentSerializer(serializers.Serializer):
    """Active incident serializer."""

    id = serializers.IntegerField()

    def to_representation(self, update: models.IncidentUpdate):
        """Get representation from IncidentUpdate."""
        incident = update.incident
        result = {
            "id": incident.incident_id,
            "title": update.title,
            "description": update.description,
            "severity": update.severity,
            "status": update.status,
            "monitor_status": update.monitor_status,
            "is_visible": update.is_visible,
            "is_enabled": update.is_enabled,
            "last_update": update.updated_at,
        }
        return result


class ActiveIncidentsSerializer(serializers.Serializer):
    """Active incidents (list) serializer."""

    results = ActiveIncidentSerializer(many=True)
    counts = IncidentCountsSerializer()

    def to_representation(self, updates):
        """Get representation from IncidentUpdate QuerySet."""
        serializer = ActiveIncidentSerializer
        incidents = [serializer(inc).data for inc in updates]
        counts = IncidentCountsSerializer().to_representation(updates)
        highest_severity = None
        for severity in models.IncidentSeverity:
            count = counts["severity"][severity.value]
            if count > 0:
                highest_severity = severity.value
                break
        result = {
            "highest_severity": highest_severity,
            "results": incidents,
            "counts": counts,
        }
        return result


class SystemMethodSerializer(serializers.ModelSerializer):
    """Serializer for SystemMethodField field."""

    id = serializers.IntegerField(source="system_id")
    active_incidents = SystemIncidentSummaryMethodField()

    class Meta:
        """Meta options for the serializer."""

        model = models.System
        fields = ("id", "alias", "name", "description", "active_incidents", "is_visible", "is_enabled")

    def get_active_incidents(self, system: models.System):
        """Get the value for the `active_incidents` field."""
        active_updates = system.incident_updates.filter(effective_until__gt=shortcuts.utc_now())
        return ActiveIncidentsSerializer(active_updates).data


class StatusPageSerializer(serializers.ModelSerializer):
    """Status Page Serializer."""

    categories = SystemCategoryMethodField(many=True)

    class Meta:
        """Meta options for the serializer."""

        model = models.StatusPage
        fields = ("title", "description", "categories")

    def get_categories(self, instance):
        """Get value of the categories field."""
        query_set = models.SystemCategory.objects.all().order_by("rank")
        return [SystemCategoryMethodSerializer(category).data for category in query_set]


class SystemCategoryMethodSerializer(serializers.ModelSerializer):
    """Serializser for SystemCategoryMethodField field."""

    id = serializers.IntegerField(source="system_category_id")
    systems = SystemMethodField(many=True)

    class Meta:
        """Meta options for the serializer."""

        model = models.SystemCategory
        fields = ("id", "name", "description", "is_visible", "systems")

    def get_systems(self, category: models.SystemCategory):
        """Get the value for the `systems` field."""
        systems = category.system_set.order_by("rank").all()
        return [SystemMethodSerializer(system).data for system in systems]


class StatusPageSchema(schemas.openapi.AutoSchema):  # pragma: no cover
    """AutoSchema for the Django Status Page."""

    def map_field(self, field):
        """Get the field schema."""
        if isinstance(field, StatusPageMethodField):
            mapping = {
                "type": "array",
                "items": {
                    "type": "object",
                },
            }
        else:
            mapping = super().map_field(field)

        return mapping
