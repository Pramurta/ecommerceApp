from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt

from products.models import Product, Vendor
from django.db import transaction
# Create your views here.

@csrf_exempt
@transaction.atomic
def createVendor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if "vendorName" not in data or data["vendorName"] is None or len(data["vendorName"])==0:
                return JsonResponse({"status": "failure", "message": "Vendor name not provided"}, status=500)
            existing_vendor: Vendor = Vendor.objects.filter(name=data["vendorName"]).exists()
            if existing_vendor:
                return JsonResponse({"status": "failure", "error": f"Vendor with name: {data['vendor_name']} already exists!"}, status=400)
            else:
                vendor = Vendor(name=data["vendorName"])
                vendor.save()
                return JsonResponse({"status": "success", "message": "Vendor created successfully!"})
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": f"Request failed with error: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only POST requests allowed for create operations"},status=405) 
    
@csrf_exempt
@transaction.atomic
def editVendor(request):
    if request.method == 'POST':
        try:
            update_request = json.loads(request.body)
            vendor: Vendor = get_object_or_404(Vendor, pk=update_request["vendor_id"])
            if "vendor_name" in update_request and update_request["vendor_name"] is not None and len(update_request["vendor_name"])>0:
                vendor.name = update_request["vendor_name"]
                vendor.save()
                return JsonResponse({"status": "success", "message": "Vendor name changed successfuly!"},status=200)
            else:
                return JsonResponse({"status": "failure", "message": "Vendor name not provided!"},status=400)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": f"Request failed with error: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only POST requests allowed for edit operations"},status=405)  

@csrf_exempt
@transaction.atomic
def removeVendor(request):
    if request.method == 'DELETE':
        try:
            update_request = json.loads(request.body)
            vendor: Vendor = get_object_or_404(Vendor, pk=update_request["vendor_id"])
            vendor.delete()
            return JsonResponse({"status": "success", "message": "Vendor removed successfully!"},status=204)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure", "message": f"Request failed with error: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only DELETE requests allowed for delete operations"},status=405)
    

@csrf_exempt
@transaction.atomic
def createProduct(request):
    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)
            product_name = requestBody["product_name"]
            vendor_id = requestBody["vendor_id"]
            vendor = get_object_or_404(Vendor, pk=vendor_id)
            price = requestBody["price"]
            category = requestBody["category"]
            product = Product(name=product_name, category=category, price=price, vendor=vendor)
            product.save()
            return JsonResponse({"status": "success", "message": "Product created successfully!"},status=201)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure","message": str(e)},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only POST requests allowed for create operations"},status=405) 
    
@csrf_exempt
@transaction.atomic
def removeProduct(request):
    if request.method == 'DELETE':
        try:
            requestBody = json.loads(request.body)
            product_id = requestBody["id"]
            product = get_object_or_404(Product, pk=product_id)
            product.delete()
            return JsonResponse({"status": "success","message": "Product removed successfully!"},status=204)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure","message": str(e)},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only DELETE requests allowed for delete operations"},status=405)
    
@csrf_exempt
@transaction.atomic
def editProduct(request):
    if request.method == 'POST':
        try:
            requestBody = json.loads(request.body)
            if "id" not in requestBody or requestBody["id"] is None or len(requestBody["id"])==0:
                return JsonResponse({"status": "failure", "message": "Product ID not provided"},status=400)
            product_id = requestBody["id"]
            product = get_object_or_404(Product, pk=product_id)
            if "name" in requestBody and requestBody["name"] is not None and len(requestBody["name"])>0:
                product.name = requestBody["name"]
            if "category" in requestBody and requestBody["category"] is not None and len(requestBody["category"])>0:
                product.category = requestBody["category"]
            if "price" in requestBody and requestBody["price"] is not None and len(requestBody["price"])>0:
                product.price = requestBody["price"]
            
            product.save()

            return JsonResponse({"status": "success","message": "Product details edited successfully!"},status=200)
        except Exception as e:
            transaction.set_rollback(True)
            return JsonResponse({"status": "failure","message": str(e)},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only POST requests allowed for edit operations"},status=405)




    


