from django.urls import path
from . import views

urlpatterns = [
    path('createOrder/',views.createOrder),
    path('cancelOrder/',views.cancelOrder)
]
