from django.forms import ValidationError
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout

from users.models import Customer
# Create your views here.

@csrf_exempt
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

            customer = Customer(passportNumber=requestBody["passportNumber"], 
                                password=requestBody["password"], 
                                email=requestBody["email"])
            
            customer.full_clean()
            
            customer.save()

            customer_dict = model_to_dict(customer)
        
            return JsonResponse({"status": "success", "message": "User created successfully!", "user": customer_dict}, status=201)
        
        except ValidationError as e:
            errors = dict(e)
            return JsonResponse({"status": "failure", "message": "Validation error", "errors": errors}, status=400)
        
        except Exception as e:
            return JsonResponse({"status": "failure", "message": str(e)}, status=500)
    
    else:
        return JsonResponse({"status": "failure", "message": "Only post requests allowed for this endpoint!"},
                             status=405)
    
# @csrf_exempt
# def login(request):
#     if request.method == "POST":
#         requestBody = json.loads(request.body)
#         username = requestBody["username"]
#         password = requestBody["password"]
#         user = authenticate(request, username=username, password=password)
#     else:
#         return JsonResponse({"status": "failure", "message": "Only post requests allowed for this endpoint!"},
#                              status=405)
    
    


    
