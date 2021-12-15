from django.contrib import admin

from . import models

class IncidentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )
    list_display = ('incident_id', 'origin', 'id_at_origin', 'created_at', 'created_by' )

    def save_model(self, request, obj: models.BaseModel, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.Incident, IncidentAdmin)