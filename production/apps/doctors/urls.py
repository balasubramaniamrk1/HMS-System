from django.urls import path
from . import views, views_console

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('console/', views_console.doctor_console, name='doctor_console'), # New Console
    path('specialities/', views.department_list, name='department_list'),
    path('specialities/<slug:slug>/', views.department_detail, name='department_detail'),
]
