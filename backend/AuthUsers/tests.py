from django.test import TestCase
from .models import Customer

class CustomerModelTest(TestCase):
    def test_create_customer(self):
        customer = Customer.objects.create(
            clerk_id="123456",
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(customer.email, "test@example.com")
