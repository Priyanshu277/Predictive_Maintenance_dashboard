import os
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from django.conf import settings
import pandas as pd
from .models import Sensordata


def prepare_data():
    # Fetch sensor data from the database
    sensor_data = list(Sensordata.objects.values('temperature', 'vibration', 'timestamp'))

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


def train_model():
    X, y = prepare_data()
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def save_model(model):
    model_path = os.path.join(settings.BASE_DIR, 'mypmd', 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
