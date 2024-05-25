from django.db import models
from django.core.validators import RegexValidator
import uuid
from products.models import Product
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.

class Customer(models.Model):

    passportNumber = models.CharField(max_length=200, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=2000)
    delivery_address = models.CharField(max_length=2000, default=None)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField()




    
    