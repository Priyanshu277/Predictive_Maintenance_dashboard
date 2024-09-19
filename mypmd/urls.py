from django.urls import path
from . import views

app_name = 'mypmd'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/<int:machine_id>/', views.dashboard, name='dashboard_with_machine'),
]
