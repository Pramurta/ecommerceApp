from django.db import models
from django.core.validators import RegexValidator
from django.db.models import UniqueConstraint

from products.models import Product


# Create your models here.

class Customer(models.Model):
    password_validator = RegexValidator(
        regex=r'^[\w]{3,30}$',
        message="Password must be 3-30 characters long and can only contain letters, numbers, and underscores."
    )

    passportNumber = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(validators=[password_validator], max_length=30)
    delivery_address = models.CharField(max_length=2000, default=None)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['customer', 'product'], name='unique_customer_product')
        ]

    
    