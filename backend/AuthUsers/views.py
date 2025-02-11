from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from svix.webhooks import WebhookVerificationError, Webhook # Keep this, 'Webhooks' is correct
import json
from .models import Customer  # Import the Customer model
import logging
logger = logging.getLogger(__name__)



@csrf_exempt
def clerk_webhook(request):
    logger.info("Webhook received!")
    
    if request.method == "POST":
        payload = request.body
        headers = request.headers
        wh = Webhook("whsec_d/ljJQoq/PgNzOEGaebcY26VK6+I3lus")  # Replace with your secret

        try:
            verified_payload = wh.verify(payload, headers)
            event = json.loads(verified_payload)
            
            logger.info(f"Webhook event received: {event}")

            user_data = event["data"]["object"]
            clerk_id = user_data["id"]
            email = user_data["email_addresses"][0]["email_address"]
            first_name = user_data.get("first_name", "")
            last_name = user_data.get("last_name", "")

            if event["type"] == "user.created":
                Customer.objects.update_or_create(
                    clerk_id=clerk_id,
                    defaults={"email": email, "first_name": first_name, "last_name": last_name},
                )

            elif event["type"] == "user.updated":
                Customer.objects.filter(clerk_id=clerk_id).update(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )

            elif event["type"] == "user.deleted":
                Customer.objects.filter(clerk_id=clerk_id).delete()

            return JsonResponse({"status": "success"}, status=200)
        except WebhookVerificationError:
            return JsonResponse({"error": "Invalid signature"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
