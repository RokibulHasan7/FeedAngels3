from django.urls import path
from . import views

urlpatterns = [
    path('volunteer_signup/', views.volunteer_signup, name="volunteer_signup"),
    path('', views.VolunteerProfile, name="/"),
]