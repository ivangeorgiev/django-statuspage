from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from . import models


class SystemFilter(admin.SimpleListFilter):
    title = "system"
    parameter_name = 'system'

    def lookups(self, request, model_admin):
        qs = models.System.objects.order_by('category__name', 'name').all()
        return [(s.system_id, f'{s.category.name} > {s.name}') for s in qs]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(system_id=self.value())
        return queryset

class UpdateUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj: models.BaseModel, *args, **kwargs):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, *args, **kwargs)

class IncidentAdmin(UpdateUserAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_display = ('incident_id', 'title', 'origin', 'id_at_origin', 'created_at', 'created_by', )


class IncidentUpdateAdmin(UpdateUserAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_display = ('incident_update_id', 'incident_id', 'incident_title', 'system', 'title', 'status', 'monitor_status', 'created_at', 'effective_until', )
    list_filter = ('status', 'monitor_status', SystemFilter)
    ordering = ('-created_at', 'incident')

    def incident_title(self, obj):
        return obj.incident.title

    def system(self, obj):
        return obj.affected_system.name

class SystemAdmin(UpdateUserAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_display = ('system_id', 'effective_rank', 'alias', 'category', 'name', 'is_visible', 'is_enabled',)
    ordering = ('category', 'name', )

    @admin.display(ordering=Concat('category__rank', Value(' '), 'rank'))
    def effective_rank(self, obj):
        return f'{obj.category.rank}-{obj.rank}'

class SystemCategoryAdmin(UpdateUserAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_display = ('system_category_id', 'rank', 'name', 'is_visible',)
    ordering = ('name', )


admin.site.register(models.Incident, IncidentAdmin)
admin.site.register(models.System, SystemAdmin)
admin.site.register(models.SystemCategory, SystemCategoryAdmin)
admin.site.register(models.IncidentUpdate, IncidentUpdateAdmin)