from django.contrib import admin

from . import models

class SaveUserAdminMixin(admin.ModelAdmin):
    def save_model(self, request, obj: models.BaseModel, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super(admin.ModelAdmin, self).save_model(request, obj, form, change)


class IncidentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', )

    def save_model(self, request, obj: models.BaseModel, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.Incident, IncidentAdmin)