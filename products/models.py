from django.db import models
import uuid
from users.models import Customer


# Create your models here.
class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)

class Product(models.Model):
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()