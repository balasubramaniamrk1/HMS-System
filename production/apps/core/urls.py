from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('role-redirect/', views.role_based_redirect, name='role_redirect'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('packages/', views.package_list, name='package_list'),
    path('careers/', views.careers, name='careers'),
    path('international/', views.international, name='international'),
    path('insurance/', views.insurance_tpa, name='insurance'),
]
