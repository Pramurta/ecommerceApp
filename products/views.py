from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt

from products.models import Vendor
# Create your views here.

@csrf_exempt
def createVendor(request):
    data = json.loads(request.body)
    if "vendorName" not in data or data["vendorName"] is None or len(data["vendorName"])==0:
        return JsonResponse({"status": "failure", "message": "Vendor name not provided"}, status=500)
    vendor = Vendor(name=data["vendorName"])
    vendor.full_clean()
    vendor.save()
    return JsonResponse({"status": "success", "message": "Vendor created successfully!"})
    
@csrf_exempt
def editVendor(request):
    if request.method == 'POST':
        try:
            update_request = json.loads(request.body)
            vendor: Vendor = get_object_or_404(Vendor, pk=update_request["vendor_id"])
            if "vendor_name" in update_request and update_request["vendor_name"] is not None and len(update_request["vendor_name"])>0:
                vendor.name = update_request["vendor_name"]
                vendor.save()
                return JsonResponse({"status": "success", "message": "Vendor name changed successfuly!"},status=200)
        except Exception as e:
            return JsonResponse({"status": "failure", "message": f"Request failed with error: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only POST requests allowed for edit operations"},status=405)  

@csrf_exempt
def removeVendor(request):
    if request.method == 'DELETE':
        try:
            update_request = json.loads(request.body)
            vendor: Vendor = get_object_or_404(Vendor, pk=update_request["vendor_id"])
            vendor.delete()
            return JsonResponse({"status": "success", "message": "Vendor removed successfully!"},status=204)
        except Exception as e:
            return JsonResponse({"status": "failure", "message": f"Request failed with error: {str(e)}"},status=500)
    else:
        return JsonResponse({"status": "failure", "message": "Only DELETE requests allowed for delete operations"},status=405)

    

