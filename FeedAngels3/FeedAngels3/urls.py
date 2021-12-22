"""HomeAway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin

from part1 import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('test/', views.test, name='test'),
    path('pickuppoints/', views.pickup, name='pickup'),
    path('volunteersignup/<int:userid>', views.volunteerSignUp, name='VolunteerSignup'),
    path('VolunteerProfile/<int:volunteerId>', views.VolunteerProfile, name='VolunteerProfile'),
    path('userProfile/<int:userid>', views.UserProfile, name='userProfile'),
    path('changePassword/', views.change_password, name='changePassword'),
    path('password_reset/', views.password_reset_request, name="password_reset"),
    #path('password_reset', auth_views.PasswordResetView.as_view(template_name='auth/password/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password/password_reset_complete.html'), name='password_reset_complete'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('pickupPointSearchResult/', views.pickupPointSearchResult.as_view(), name='pickupPointSearchResult'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)