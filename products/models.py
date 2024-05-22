from django.db import models
import uuid


# Create your models here.
class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    price = models.FloatField(default=10)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
