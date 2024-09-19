from django.contrib import admin
from .models import Equipment, Sensordata

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'equipment_type', 'installation_date')
    search_fields = ('name', 'equipment_type')

@admin.register(Sensordata)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'timestamp', 'temperature', 'vibration')
    list_filter = ('equipment', 'timestamp')
    search_fields = ('equipment__name',)

