from django.urls import path
from contact import views

urlpatterns = [
    path('contact_us/', views.contact_us, name='contact_us'),
]