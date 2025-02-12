from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.cache import cache
import jwt
from datetime import datetime, timedelta
from AuthUsers.middlewares import JWTAuthenticationMiddleware
from django.test import RequestFactory

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def generate_jwt(self, user_id):
        """Helper function to generate test JWT"""
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "email": "test@example.com",
        }
        return jwt.encode(payload, "testsecret", algorithm="HS256")

    def test_jwt_authentication(self):
        """Test if JWT authentication middleware works"""
        token = self.generate_jwt(self.user.id)
        request = self.factory.get("/", HTTP_AUTHORIZATION=f"Bearer {token}")
        middleware = JWTAuthenticationMiddleware()
        
        user, _ = middleware.authenticate(request)
        self.assertEqual(user.email, "test@example.com")
