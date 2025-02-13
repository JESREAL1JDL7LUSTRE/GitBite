import json
import logging
import environ
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from svix.webhooks import Webhook, WebhookVerificationError
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


logger = logging.getLogger(__name__)

# ✅ Load environment variables properly
env = environ.Env()
env.read_env()
CLERK_WEBHOOK_SECRET = env.str("CLERK_WEBHOOK_SECRET")

@csrf_exempt
def clerk_webhook(request):
    logger.info("Webhook received!")

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    payload = request.body
    headers = request.headers

    try:
        # ✅ Verify the webhook payload
        wh = Webhook(CLERK_WEBHOOK_SECRET)
        verified_payload = wh.verify(payload, headers)
        print("Webhook Data:", payload)

        # ✅ Ensure verified_payload is a dictionary
        if isinstance(verified_payload, str):
            verified_payload = json.loads(verified_payload)

        if not isinstance(verified_payload, dict):
            logger.error("Webhook payload is not a dictionary")
            return JsonResponse({"error": "Invalid webhook format"}, status=400)

        # ✅ Use `data` directly instead of `.get("object")`
        user_data = verified_payload.get("data", {})

        if not isinstance(user_data, dict):
            logger.error(f"Webhook 'data' field is not a dictionary: {user_data}")
            return JsonResponse({"error": "Invalid webhook data"}, status=400)

        # ✅ Extract fields correctly
        clerk_id = user_data.get("id", "")
        email = user_data.get("email_addresses", [{}])[0].get("email_address", "")
        first_name = user_data.get("first_name", "")
        last_name = user_data.get("last_name", "")

        if not clerk_id:
            logger.error("Webhook event missing 'id' field")
            return JsonResponse({"error": "Invalid webhook payload"}, status=400)

        # ✅ Process user created/updated/deleted events
        event_type = verified_payload.get("type", "")

        if event_type == "user.created":
            Customer.objects.update_or_create(
                clerk_id=clerk_id,
                defaults={"email": email, "first_name": first_name, "last_name": last_name},
            )

        elif event_type == "user.updated":
            Customer.objects.filter(clerk_id=clerk_id).update(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

        elif event_type == "user.deleted":
            Customer.objects.filter(clerk_id=clerk_id).delete()

        return JsonResponse({"status": "success"}, status=200)

    except WebhookVerificationError:
        logger.error("Invalid webhook signature")
        return JsonResponse({"error": "Invalid signature"}, status=400)

    except json.JSONDecodeError:
        logger.error("Webhook JSON decoding failed")
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Customer

class LoggedInCustomerView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ Requires authentication

    def get(self, request):
        try:
            customer = Customer.objects.get(email=request.user.email)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from rest_framework.authentication import BaseAuthentication

@api_view(["GET"])
@authentication_classes([BaseAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        print("User:", request.user)  # Debugging
        print("Email:", request.user.email)  # Debugging

        customer = Customer.objects.get(email=request.user.email)
        return JsonResponse({
            "id": customer.clerk_id,
            "email": customer.email,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
        })
    except Customer.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
