"""Customize Django admin interface."""

from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from . import config, models

site = admin.site

site.site_header = config.ADMIN_SITE_HEADER
site.site_title = config.ADMIN_SITE_TITLE
site.index_title = config.ADMIN_INDEX_TITLE


class SystemFilter(admin.SimpleListFilter):
    """List filter by systems."""

    title = "system"
    parameter_name = "system"

    def lookups(self, request, model_admin):
        """Get a list of systems."""
        qs = models.System.objects.order_by("category__name", "name").all()
        return [(s.system_id, f"{s.category.name} > {s.name}") for s in qs]

    def queryset(self, request, queryset):
        """Filter a queryset."""
        if self.value():
            return queryset.filter(system_id=self.value())
        return queryset


class UpdateUserAdmin(admin.ModelAdmin):
    """Abstract ModelAdmin class which maintains created_by and updated_by model fields."""

    def save_model(self, request, obj: models.BaseModel, *args, **kwargs):
        """Override original save_model method to update created_by and updatd_by model fields."""
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, *args, **kwargs)


class IncidentAdmin(UpdateUserAdmin):
    """ModelAdmin for Incident model."""

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_display = (
        "incident_id",
        "title",
        "origin",
        "id_at_origin",
        "created_at",
        "created_by",
    )


class IncidentUpdateAdmin(UpdateUserAdmin):
    """ModelAdmin for IncidentUpdate model."""

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_display = (
        "incident_update_id",
        "incident_id",
        "incident_title",
        "system",
        "title",
        "status",
        "monitor_status",
        "created_at",
        "effective_until",
    )
    list_filter = ("status", "monitor_status", SystemFilter)
    ordering = ("-created_at", "incident")

    def incident_title(self, obj):
        """Calculate ``incident title`` field."""
        return obj.incident.title

    def system(self, obj):
        """Calculate ``system`` field."""
        return obj.affected_system.name


class SystemAdmin(UpdateUserAdmin):
    """ModelAdmin for System model."""

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_display = (
        "system_id",
        "effective_rank",
        "alias",
        "category",
        "name",
        "is_visible",
        "is_enabled",
    )
    ordering = (
        "category",
        "name",
    )

    @admin.display(ordering=Concat("category__rank", Value(" "), "rank"))
    def effective_rank(self, obj):
        """Calculate ``effective rank`` field."""
        return f"{obj.category.rank}-{obj.rank}"


class SystemCategoryAdmin(UpdateUserAdmin):
    """ModelAdmin for SystemCategory model."""

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_display = (
        "system_category_id",
        "rank",
        "name",
        "is_visible",
    )
    ordering = ("name",)


class StatusPageAdmin(UpdateUserAdmin):
    """Admin for Status Page model."""

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    list_display = (
        "title",
        "created_by",
        "updated_by",
        "updated_at",
    )

    def has_add_permission(self, *args, **kwargs):
        """Disable StatusPage object creation from the UI."""
        return False

    def has_delete_permission(self, *args, **kwargs):
        """Disable StatusPage object deletion from the UI."""
        return False


admin.site.register(models.Incident, IncidentAdmin)
admin.site.register(models.StatusPage, StatusPageAdmin)
admin.site.register(models.System, SystemAdmin)
admin.site.register(models.SystemCategory, SystemCategoryAdmin)
admin.site.register(models.IncidentUpdate, IncidentUpdateAdmin)
