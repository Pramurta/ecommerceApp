
from django.http import JsonResponse
from users.models import Customer
from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
import re

def generate_jwt_token(customer: Customer):
    payload = {
        "passportNumber": customer.passportNumber,
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

def validate_password(raw_password: str):
    pattern = re.compile(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$'
    )
    
    # Match the password against the pattern
    if not pattern.match(raw_password):
        return False
    
    return True