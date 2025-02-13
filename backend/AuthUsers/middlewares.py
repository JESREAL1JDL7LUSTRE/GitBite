# middleware.py
import datetime
from datetime import datetime
import environ
import jwt
import pytz
import requests
from django.contrib.auth.models import User
from django.core.cache import cache
from jwt.algorithms import RSAAlgorithm
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Customer

env = environ.Env()

CLERK_API_URL = "https://api.clerk.com/v1"
CLERK_FRONTEND_API_URL = env("CLERK_FRONTEND_API_URL")
CLERK_SECRET_KEY = env("CLERK_SECRET_KEY")
CACHE_KEY = "jwks_data"


class JWTAuthenticationMiddleware(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        try:
            if not auth_header or " " not in auth_header:
                raise AuthenticationFailed("Invalid Authorization header format.")

            token = auth_header.split(" ")[1]  # ✅ Fix
        except IndexError:
            raise AuthenticationFailed("Bearer token not provided.")
        user = self.decode_jwt(token)
        clerk = ClerkSDK()
        info, found = clerk.fetch_user_info(user.clerk_id)
        if not user:
            return None
        else:
            if found:
                user.email = info["email_address"]
                user.first_name = info["first_name"]
                user.last_name = info["last_name"]
                user.last_login = info["last_login"]
            user.save()

        return user, None

    def decode_jwt(self, token):
        clerk = ClerkSDK()
        jwks_data = clerk.get_jwks()
        keys = jwks_data.get("keys", [])
        if not keys:
            raise AuthenticationFailed("No public keys found.")
        public_key = RSAAlgorithm.from_jwk(keys[0])

        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                options={"verify_signature": True},
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.DecodeError:
            raise AuthenticationFailed("Token decode error.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        user_id = payload.get("sub")
        if user_id:
            customer, created = Customer.objects.get_or_create(
                clerk_id=user_id,
                defaults={
                    "email": payload.get("email", ""),
                    "first_name": payload.get("given_name", ""),
                    "last_name": payload.get("family_name", ""),
                },
            )
            return customer  # ✅ Return Customer instead of User
        return None

class ClerkSDK:
    def fetch_user_info(self, user_id: str):
        response = requests.get(
            f"{CLERK_API_URL}/users/{user_id}",
            headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
        )
        if response.status_code == 200:
            data = response.json()
            email = data["email_addresses"][0]["email_address"]
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            last_login = datetime.datetime.fromtimestamp(
                data["last_sign_in_at"] / 1000, tz=pytz.UTC
            )

            # Store or update customer in separate table
            customer, created = Customer.objects.update_or_create(
                clerk_id=user_id,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "last_login": last_login,
                },
            )
            return {
                "email_address": customer.email,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "last_login": customer.last_login,
            }, True
        else:
            return {
                "email_address": "",
                "first_name": "",
                "last_name": None,
                "last_login": None,
            }, False

    def get_jwks(self):
        jwks_data = cache.get(CACHE_KEY)
        if not jwks_data:
            response = requests.get(f"{CLERK_FRONTEND_API_URL}/.well-known/jwks.json")
            if response.status_code == 200:
                jwks_data = response.json()
                cache.set(CACHE_KEY, jwks_data)  # cache indefinitely
            else:
                raise AuthenticationFailed("Failed to fetch JWKS.")
        return jwks_data