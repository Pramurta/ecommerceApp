from django.urls import path

from users import views

urlpatterns = [
    path('signup/',views.signup),
    path('login/',views.login),
    path('addToCart/',views.add_to_cart),
    path('removeFromCart/',views.remove_from_cart)
]
