"""Schemas module."""
from rest_framework import schemas, serializers

from . import models

# TODO(ig): Implement open-api (https://github.com/ivangeorgiev/django-statuspage/issues/9)


class StatusPageMethodField(serializers.SerializerMethodField):
    """Abstract method field."""

    many: False


class SystemCategoriesMethodField(StatusPageMethodField):
    """System categories method field."""

    many = True


class SystemsMethodField(StatusPageMethodField):
    """Systems method field."""

    many = True


class SystemStatusMethodField(StatusPageMethodField):
    """System status method field."""

    pass


class SystemMethodSerializer(serializers.ModelSerializer):
    """Serializer for SystemMethodField field."""

    id = serializers.IntegerField(source="system_id")
    status = SystemStatusMethodField()

    class Meta:
        """Meta options for the serializer."""

        model = models.System
        fields = ("id", "alias", "category", "name", "description", "status", "is_visible", "is_enabled")

    def get_status(self, system: models.System):
        """Get the value for the `status` field."""
        updates = system.incident_updates.all()
        return [u.title for u in updates]


class StatusPageSerializer(serializers.ModelSerializer):
    """Status Page Serializer."""

    categories = SystemCategoriesMethodField()
    systems = SystemsMethodField()

    class Meta:
        """Meta options for the serializer."""

        model = models.StatusPage
        fields = ("title", "description", "categories", "systems")

    def get_categories(self, instance):
        """Get value of the categories field."""
        query_set = models.SystemCategory.objects.all().order_by("rank")
        return [SystemCategoryMethodSerializer(category).data for category in query_set]

    def get_systems(self, instance):
        """Get value of the systems field."""
        query_set = models.System.objects.all().order_by("category__rank", "rank")
        return [SystemMethodSerializer(system).data for system in query_set]


class SystemCategoryMethodSerializer(serializers.ModelSerializer):
    """Serializser for SystemCategoryMethodField field."""

    id = serializers.IntegerField(source="system_category_id")

    class Meta:
        """Meta options for the serializer."""

        model = models.SystemCategory
        fields = ("id", "name", "description", "is_visible")


class StatusPageSchema(schemas.openapi.AutoSchema):
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
