import jwt
from django.http import JsonResponse
from functools import wraps
from .models import Customer
from django.conf import settings

def jwt_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Extract the JWT token from the request headers
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return JsonResponse({"staus": "failure", "message": "Authorization header missing"}, status=401)

        token = authorization_header.split(' ')[1] if ' ' in authorization_header else None

        if not token:
            return JsonResponse({"error": "Invalid token"}, status=401)

        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Retrieve the user using the passportNumber from the JWT token payload
            passport_number = payload.get('passportNumber')
            user = Customer.objects.get(passportNumber=passport_number)

            # Attach the user object to the request
            request.user = user

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=401)

        # Call the view function if JWT authentication is successful
        return view_func(request, *args, **kwargs)

    return _wrapped_view
