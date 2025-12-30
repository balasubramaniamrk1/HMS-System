from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.public_reviews, name='public_reviews'),
]
