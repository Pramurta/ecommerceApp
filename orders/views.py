from typing import List
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
import uuid
from orders.models import Order, OrderItem, OrderStatus, PaymentStatus
from products.models import Product
from users.models import Cart, Customer
from users.decorators import jwt_auth_required
from django.db import transaction


@csrf_exempt
@jwt_auth_required
@transaction.atomic
def createOrder(request):
    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)
            customer_id = requestBody["customer_id"]
            product_ids = requestBody["product_ids"]
            order_id = uuid.uuid4()
            customer: Customer = get_object_or_404(Customer, pk=customer_id)
            totalPrice = 0

            for product_id in product_ids:
                product_obj: Product = get_object_or_404(Product, pk=product_id)

                cartItem_qs = Cart.objects.filter(product=product_obj, customer=customer)

                if cartItem_qs.exists():
                    cartItem = cartItem_qs.first()
                    orderItem = OrderItem(order_id=order_id, product=product_obj,
                                    quantity=cartItem.quantity, price=product_obj.price)
                    cartItem.delete()
                else:
                    return JsonResponse({"status": "failure", "message": f"Order item of customer: {customer.passportNumber}, product: {product_obj.name} doesn't exist in user's cart."})
                
                orderItem.save()
                totalPrice+=product_obj.price

            
            order: Order = Order(order_id=order_id, 
                                customer=customer,
                                order_status=OrderStatus.ORDER_PLACED,
                                total_amount_paid=totalPrice,
                                delivery_address = customer.delivery_address,
                                payment_status = PaymentStatus.NOT_STARTED)
            order.save()

            return JsonResponse({"status": "success", "message": "Order created successfully!"},status=201)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": f"Process failed with: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only post requests allowed for this endpoint!"},
                             status=405)


@csrf_exempt
@jwt_auth_required
@transaction.atomic
def cancelOrder(request):
    if request.method == 'DELETE':
        try:
            requestBody = json.loads(request.body)
            order_id = requestBody["order_id"]
            order: Order = get_object_or_404(Order, pk=order_id)
            order.delete()
            orderItems = OrderItem.objects.filter(order_id=order_id)
            orderItems.delete()
            return JsonResponse({"status": "success", "message": f"Order ID: {order_id} cancelled successfully!"})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": f"Process failed with: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only delete requests allowed for this endpoint!"},
                             status=405)

