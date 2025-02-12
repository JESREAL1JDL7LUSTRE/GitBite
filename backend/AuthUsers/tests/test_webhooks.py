from django.test import TestCase, Client
from django.urls import reverse
from AuthUsers.models import Customer
import json

class ClerkWebhookTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.webhook_url = reverse("clerk_webhook")

    def test_user_created_webhook(self):
        """Test if a 'user.created' event adds a customer"""
        payload = {
            "type": "user.created",
            "data": {
                "object": {
                    "id": "clerk_12345",
                    "email_addresses": [{"email_address": "test@example.com"}],
                    "first_name": "John",
                    "last_name": "Doe",
                }
            },
        }
        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Customer.objects.filter(clerk_id="clerk_12345").exists())

    def test_user_updated_webhook(self):
        """Test if a 'user.updated' event updates a customer"""
        customer = Customer.objects.create(
            clerk_id="clerk_12345", email="old@example.com", first_name="Old", last_name="Name"
        )

        payload = {
            "type": "user.updated",
            "data": {
                "object": {
                    "id": "clerk_12345",
                    "email_addresses": [{"email_address": "new@example.com"}],
                    "first_name": "New",
                    "last_name": "User",
                }
            },
        }
        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        customer.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(customer.email, "new@example.com")
        self.assertEqual(customer.first_name, "New")
        self.assertEqual(customer.last_name, "User")

    def test_user_deleted_webhook(self):
        """Test if a 'user.deleted' event removes a customer"""
        customer = Customer.objects.create(
            clerk_id="clerk_12345", email="test@example.com", first_name="John", last_name="Doe"
        )

        payload = {
            "type": "user.deleted",
            "data": {"object": {"id": "clerk_12345"}},
        }
        response = self.client.post(
            self.webhook_url,
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Customer.objects.filter(clerk_id="clerk_12345").exists())
