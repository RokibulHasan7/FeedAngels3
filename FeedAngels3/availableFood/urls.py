from django.urls import path
from availableFood import views

urlpatterns = [
    path('availableFood/', views.availableFood, name='availfood'),
]