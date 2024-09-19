from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=100)
    installation_date = models.DateField()

    def __str__(self):
        return self.name
    
class Sensordata(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='sensor_data')
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    vibration = models.FloatField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.equipment.name} - {self.timestamp}"

