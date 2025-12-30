from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
]
