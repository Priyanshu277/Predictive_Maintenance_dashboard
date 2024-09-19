import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO
import base64
from .models import Equipment, Sensordata
import json
from .utils import prepare_data, train_model, save_model
import pickle
from django.conf import settings
import os
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta, datetime
from sklearn.preprocessing import StandardScaler


def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'mypmd', 'model.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)
    
def prepare_data_for_machine(machine):
    # Fetch sensor data from the database for the specific machine
    sensor_data = list(Sensordata.objects.filter(equipment=machine).values('temperature', 'vibration', 'timestamp'))

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(sensor_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Engineer features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_of_week
    df['month'] = df['timestamp'].dt.month

    # Split into features and target
    X = df[['temperature', 'vibration', 'hour', 'day_of_week', 'month']].values
    y = (df['vibration'] > df['vibration'].mean()).astype(int)  # Binary target for maintenance prediction

    # Standardize the features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    return X, y

def predict_maintenance(machine):
    model = load_model()
    X, _ = prepare_data_for_machine(machine)
    
    if X.size == 0:
        return 0  # Return 0 if there's no data for the machine
    
    probabilities = model.predict_proba(X)[:, 1]  # Probability of needing maintenance

    # Calculate the percentage of equipment likely to need maintenance
    maintenance_percentage = np.mean(probabilities) * 100

    return maintenance_percentage



def dashboard(request,machine_id=None):
    machines = Equipment.objects.all()

    if machine_id is None:
        current_machine = machines.first()
    else:
        current_machine = get_object_or_404(Equipment, id=machine_id)
    
    # Fetch data for the current machine
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    sensor_data = Sensordata.objects.filter(
        equipment=current_machine,
        timestamp__range=(start_date, end_date)
    ).order_by('timestamp')
    
    timestamps = [data.timestamp for data in sensor_data]
    temperatures = [data.temperature for data in sensor_data]
    vibrations = [data.vibration for data in sensor_data]
    
    scatter_data = [{"x": temp, "y": vib} for temp, vib in zip(temperatures, vibrations)]

    maintenance_percentage = predict_maintenance(current_machine)
    
    context = {
        'machines': machines,
        'current_machine': current_machine,
        'timestamps': json.dumps([t.isoformat() for t in timestamps]),
        'temperatures': json.dumps(temperatures),
        'vibrations': json.dumps(vibrations),
        'scatter_data': json.dumps(scatter_data),
        'maintenance_percentage': maintenance_percentage,
    }
    
    return render(request, 'dashboard.html', context)


