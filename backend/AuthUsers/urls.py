from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import clerk_webhook
from AuthUsers.serializers import CustomerViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"customers", CustomerViewSet, basename="customers") 

urlpatterns = [
    path("", include(router.urls)),  
    path("webhooks/", clerk_webhook, name="clerk_webhook"), 
]
