from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from orders import helpers
from django.shortcuts import get_object_or_404
import uuid
from orders.models import Order, OrderItem, OrderStatus, PaymentStatus
from products.models import Product
from users.models import Customer
# Create your views here.

@csrf_exempt
def createOrder(request):
    try:
        requestBody = json.loads(request.body)
        customer_id = requestBody["customer_id"]
        products = requestBody["products"]
        totalPrice = helpers.calculateTotalPrice(products)
        order_id = uuid.uuid4()
        customer: Customer = get_object_or_404(Customer, pk=customer_id)

        for product in products:
            product_id = product["id"]
            
            product_obj: Product = get_object_or_404(Product, pk=product_id)
            quantity = product["quantity"]
            orderItem: OrderItem = OrderItem(order_id=order_id, product=product_obj,
                                  quantity=quantity, price=product_obj.price)
            orderItem.save()
        
        order: Order = Order(order_id=order_id, 
                             customer=customer,
                             order_status=OrderStatus.ORDER_PLACED,
                             total_amount_paid=totalPrice,
                             delivery_address = customer.delivery_address,
                             payment_status = PaymentStatus.NOT_STARTED
                             )
        order.save()

        #TODO: add more validations and the logic to remove items from cart via kafka message

        return JsonResponse({"message": "Order created successfully!"})
    except Exception as e:
        return JsonResponse({"message": f"Process failed with: {str(e)}"})
