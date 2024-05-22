from enum import Enum
from django.db import models

from products.models import Product
from users.models import Customer

# Create your models here.

class OrderStatus(Enum):
    DELIVERED = 'DELIVERED'
    SHIPPED = 'SHIPPED'
    AT_SORTING_FACILITY = 'AT_SORTING_FACILITY'
    DELIVERY_ON_THE_WAY = 'DELIVERY_ON_THE_WAY'

class PaymentStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    

class Order(models.Model):
    order_id = models.UUIDField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=200, choices=[(status.name, status.value) for status in OrderStatus])
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_amount_paid = models.FloatField()
    delivery_address = models.CharField(max_length=2000)
    payment_status = models.CharField(max_length=50, choices=[(status.name, status.value) for status in PaymentStatus])


class OrderItem(models.Model):
    order_id = models.UUIDField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

