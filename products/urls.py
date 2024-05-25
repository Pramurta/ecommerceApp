from django.urls import path
from products import views

urlpatterns = [
    path('createVendor/',views.createVendor),
    path('editVendor/', views.editVendor),
    path('removeVendor/', views.removeVendor),
    path('createProduct/',views.createProduct),
    path('editProduct/',views.editProduct),
    path('removeProduct/',views.removeProduct),
]
