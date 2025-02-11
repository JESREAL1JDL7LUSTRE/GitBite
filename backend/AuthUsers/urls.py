from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from AuthUsers.serializers import UserViewSet
from .views import *


router = DefaultRouter()
router.register(r"users", UserViewSet, basename='users')
router.register(r"Customer", UserViewSet, basename='Customer')

urlpatterns = [
    path("api/", include(router.urls)),
    path("clerk-webhook/", clerk_webhook, name="clerk_webhook"),
]