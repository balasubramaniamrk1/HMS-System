from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('', views.admission_dashboard, name='dashboard'),
    path('admit/', views.admit_patient, name='admit_patient'),
    path('discharge/<int:admission_id>/', views.discharge_patient, name='discharge_patient'),
]
