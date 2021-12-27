from django.urls import path
from .views import initiate_payment, callback, donation, donateFoodView
urlpatterns = [
    path('donation/', donation, name='donation'),
    path('donateMoney/', initiate_payment, name='donateMoney'),
    path('callback/', callback, name='callback'),
    path('donateFood/<int:userid>', donateFoodView, name='donateFood'),
]


