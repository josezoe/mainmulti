from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet  # Assuming you have this view

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('', include(router.urls)),
]