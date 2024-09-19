import os
import django
import numpy as np
import pandas as pd
from datetime import timedelta

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pmd.settings")
django.setup()

from mypmd.models import Equipment, Sensordata

def generate_sensor_data(equipment, days, failure_probability=0.01):
    end_date = django.utils.timezone.now()
    start_date = end_date - timedelta(days=days)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='10T')  # Every 10 minutes
    
    temperature = np.random.normal(60, 5, len(timestamps))
    vibration = np.random.normal(0.5, 0.1, len(timestamps))
    
    # Simulate gradual degradation
    degradation = np.linspace(0, 0.5, len(timestamps))
    temperature += degradation
    vibration += degradation * 0.2
    
    # Simulate random failures
    failures = np.random.choice([0, 1], size=len(timestamps), p=[1-failure_probability, failure_probability])
    temperature += failures * np.random.normal(20, 5, len(timestamps))
    vibration += failures * np.random.normal(1, 0.2, len(timestamps))
    
    # Create SensorData objects
    sensor_data = [
        Sensordata(
            equipment=equipment,
            timestamp=timestamp,
            temperature=temp,
            vibration=vib
        )
        for timestamp, temp, vib in zip(timestamps, temperature, vibration)
    ]
    
    # Bulk create the sensor data
    Sensordata.objects.bulk_create(sensor_data)

def main():
    # Create or get an equipment
    machines = [
        {"name": "Machine 1", "type": "Pump"},
        {"name": "Machine 2", "type": "Compressor"},
        {"name": "Machine 3", "type": "Motor"},
    ]

    for machine in machines:
        equipment, created = Equipment.objects.get_or_create(
            name=machine["name"],
            equipment_type=machine["type"],
            installation_date="2024-01-01"
        )
        
        # Generate 30 days of data for each machine
        generate_sensor_data(equipment, days=30)
        print(f"Generated data for {equipment.name}")

if __name__ == "__main__":
    main()