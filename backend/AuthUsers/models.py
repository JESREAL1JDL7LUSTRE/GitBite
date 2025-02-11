from django.db import models

class Customer(models.Model):
    clerk_id = models.CharField(max_length=255, unique=True)  # Unique Clerk user ID
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email
