from typing import List
from django.forms import ValidationError
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from products.models import Product
from users.decorators import jwt_auth_required
from users.models import Cart, Customer
from users import utils
from django.core.cache import cache
from django.db import transaction
# Create your views here.

@csrf_exempt
@transaction.atomic
def signup(request):

    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)

            if "passportNumber" not in requestBody or requestBody["passportNumber"] is None or len(requestBody["passportNumber"])==0:
                return JsonResponse({"status": "failure", "message": "Passport Number not provided"}, status=500)
            
            if "password" not in requestBody or requestBody["password"] is None or len(requestBody["password"])==0:
                return JsonResponse({"status": "failure", "message": "Password not provided"}, status=500)
            
            if "email" not in requestBody or requestBody["email"] is None or len(requestBody["email"])==0:
                return JsonResponse({"status": "failure", "message": "Email not provided"}, status=500)
            
            if "delivery_address" not in requestBody or requestBody["delivery_address"] is None or len(requestBody["delivery_address"])==0:
                return JsonResponse({"status": "failure", "message": "Delivery address not provided"}, status=500)
            
            is_password_valid: bool = utils.validate_password(requestBody["password"])

            if not is_password_valid:
                return JsonResponse({ "status": "failure", 
                             "message": "Password must be 8-30 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character." })

            customer = Customer(passportNumber=requestBody["passportNumber"], 
                                password=requestBody["password"], 
                                email=requestBody["email"],
                                delivery_address=requestBody["delivery_address"])
            
            customer.full_clean()
            
            customer.save()

            customer_dict = model_to_dict(customer)
        
            return JsonResponse({"status": "success", "message": "User created successfully!", "user": customer_dict}, status=201)
        
        except ValidationError as e:
            errors = dict(e)
            return JsonResponse({"status": "failure",  "message": errors}, status=400)
        
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": str(e)}, status=500)
    
    else:
        return JsonResponse({"status": "failure", "message": "Only post requests allowed for this endpoint!"},
                             status=405)

@csrf_exempt
@transaction.atomic
def login(request):
    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)
            passportNumber = requestBody["username"]
            raw_password = requestBody["password"]
            try:
                customer = Customer.objects.get(pk=passportNumber)
                if customer.check_password(raw_password):
                    existing_token = cache.get(passportNumber)
                    if existing_token:
                        cache.delete(passportNumber)
                    token = utils.generate_jwt_token(customer)
                    cache.set(passportNumber, token, timeout=None)
                    return JsonResponse({"status": "success", "message": "Login successful!", "token": token})
                else:
                    return JsonResponse({"status": "failure", "message": "Invalid password entered"},status=401)
            except Customer.DoesNotExist:
                return JsonResponse({"status": "failure", "message": "Invalid username entered"},status=401)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Invalid request method"},status=405)

@csrf_exempt
@transaction.atomic
@jwt_auth_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)
            products = requestBody["products"]
            customer_id: str = requestBody["customer_id"]
            customer: Customer = get_object_or_404(Customer, pk=customer_id)

            carts: List[Cart] = []

            for product in products:
                product_obj: Product = get_object_or_404(Product,pk=product["id"])
                existing_cart_qs = Cart.objects.filter(customer=customer, product=product_obj)
                if existing_cart_qs.exists():
                    existing_cart: Cart = existing_cart_qs.first()
                    existing_cart.quantity = product["quantity"]
                    existing_cart.save()
                else:
                    quantity: int = product["quantity"]
                    cart: Cart = Cart(customer=customer, product=product_obj, quantity=quantity)
                    carts.append(cart)

            Cart.objects.bulk_create(carts)
            
            return JsonResponse({"status": "success","message": "Carts created/updated successfully!"},status=201)

        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure","message": str(e)},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Invalid request method"},status=405)
    
@csrf_exempt
@jwt_auth_required
@transaction.atomic
def remove_from_cart(request):
    if request.method == 'DELETE':
        try:
            requestBody = json.loads(request.body)
            product_ids = requestBody.get("product_ids",[])
            customer_id: str = requestBody.get("customer_id")
            if not product_ids or not customer_id:
                return JsonResponse({"status": "failure","message": "Customer ID and product IDs are required."},status=400)
            
            customer: Customer = get_object_or_404(Customer, pk=customer_id)

            carts_to_delete = Cart.objects.filter(customer=customer, product__in=product_ids)

            if carts_to_delete.exists():
                carts_to_delete.delete()
                return JsonResponse({"status": "success", "message": "Cart items removed successfully!"},status=200)
            
            else:
                return JsonResponse({"status": "failure", "message": "No matching cart items found to delete!"},status=400)
        
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure","message": str(e)},status=500)
        
    else:
        return JsonResponse({"status": "failure", "message": "Invalid request method"},status=405)
    
@csrf_exempt
@jwt_auth_required
@transaction.atomic
def editCart(request):
    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)

        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure","message": str(e)},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Invalid request method"},status=405)

    
    


    
