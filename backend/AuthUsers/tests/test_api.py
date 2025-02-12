from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from AuthUsers.models import Customer

class CustomerAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_list_customers(self):
        """Test retrieving customers from API"""
        Customer.objects.create(clerk_id="clerk_123", email="test@example.com")

        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_create_customer(self):
        """Test creating a customer via API"""
        data = {
            "clerk_id": "clerk_456",
            "email": "newcustomer@example.com",
        }
        response = self.client.post("/customers/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Customer.objects.filter(clerk_id="clerk_456").exists())

    def test_unauthorized_access(self):
        """Test if unauthorized access is blocked"""
        self.client.logout()
        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, 403)  # Should be forbidden
