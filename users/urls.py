from django.urls import path, include
from .views import (
    VendorSignupView, VendorProfileView, VendorDashboardView, AddUserView, VendorHomeView, VendorChangePasswordView,
    UserSignupView, user_profile, user_dashboard, update_user_profile, UserLoginView, 
    vendor_profile, vendor_dashboard, update_vendor_profile, CustomAuthToken
)
from rest_framework.authtoken import views as rest_framework_views
from . import views

app_name = 'users'

urlpatterns = [
    # Vendor-specific URLs
    path('vendor/signup/', VendorSignupView.as_view(), name='vendor_signup'),
    path('vendor/profile/', VendorProfileView.as_view(), name='vendor_profile'),
    path('vendor/dashboard/', VendorDashboardView.as_view(), name='vendor_dashboard'),
    path('vendor/add_user/', AddUserView.as_view(), name='add_user'),
    path('vendor/home/', VendorHomeView.as_view(), name='vendor_home'),
    path('vendor/change_password/', VendorChangePasswordView.as_view(), name='vendor_change_password'),

    # User-related URLs
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('profile/', user_profile, name='user_profile'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('update_profile/', update_user_profile, name='update_user_profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    # Additional vendor-specific URLs for profile and dashboard
    path('vendor/profile/view/', vendor_profile, name='view_vendor_profile'),
    path('vendor/update_profile/', update_vendor_profile, name='update_vendor_profile'),
    path('vendor/dashboard/view/', vendor_dashboard, name='view_vendor_dashboard'),
    
    # Authentication Token
    path('api-token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),

    # API endpoints
    path('api/', include([
        path('users/', views.CustomUserList.as_view(), name='user-list'),
        path('users/<int:pk>/', views.CustomUserDetail.as_view(), name='user-detail'),
        path('vendors/', views.VendorList.as_view(), name='vendor-list'),
        path('vendors/<int:pk>/', views.VendorDetail.as_view(), name='vendor-detail'),
        path('countries/', views.CountryList.as_view(), name='country-list'),
        path('countries/<int:pk>/', views.CountryDetail.as_view(), name='country-detail'),
        path('states/', views.StateList.as_view(), name='state-list'),
        path('states/<int:pk>/', views.StateDetail.as_view(), name='state-detail'),
        path('cities/', views.CityList.as_view(), name='city-list'),
        path('cities/<int:pk>/', views.CityDetail.as_view(), name='city-detail'),
        path('timezones/', views.TimezoneList.as_view(), name='timezone-list'),
        path('timezones/<int:pk>/', views.TimezoneDetail.as_view(), name='timezone-detail'),
        # New endpoints for roles, user roles, and app modules
        path('roles/', views.RoleList.as_view(), name='role-list'),
        path('roles/<int:pk>/', views.RoleDetail.as_view(), name='role-detail'),
        path('user_roles/', views.UserRoleList.as_view(), name='user_role-list'),
        path('user_roles/<int:pk>/', views.UserRoleDetail.as_view(), name='user_role-detail'),
        path('app_modules/', views.AppModuleList.as_view(), name='app_module-list'),
        path('app_modules/<int:pk>/', views.AppModuleDetail.as_view(), name='app_module-detail'),
    ])),
]

# Assuming you've added these views in your views.py or similar:
# class RoleList(generics.ListCreateAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

# class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer

# class UserRoleList(generics.ListCreateAPIView):
#     queryset = UserRole.objects.all()
#     serializer_class = UserRoleSerializer

# class UserRoleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = UserRole.objects.all()
#     serializer_class = UserRoleSerializer

# class AppModuleList(generics.ListCreateAPIView):
#     queryset = AppModule.objects.all()
#     serializer_class = AppModuleSerializer

# class AppModuleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = AppModule.objects.all()
#     serializer_class = AppModuleSerializer