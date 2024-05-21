from django.urls import path
from products import views

urlpatterns = [
    path('createVendor/',views.createVendor),
    path('editVendor/', views.editVendor),
    path('removeVendor/', views.removeVendor)
]
