from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    UserSignupView,
    VendorSignupView,
    user_profile,
    user_dashboard,
    update_user_profile,
    UserLoginView,
    vendor_profile,
    vendor_dashboard,
    update_vendor_profile,
)

app_name = 'users'

urlpatterns = [
    # User Signup URL
    path('signup/', UserSignupView.as_view(), name='signup'),

    # Vendor Signup URL
    path('vendors/signup/', VendorSignupView.as_view(), name='vendor_signup'),

    # Login URL (assuming it's the same for both user types)
    path('login/', UserLoginView.as_view(), name='login'),
    
    # Logout URL 
    path('logout/', auth_views.LogoutView.as_view(next_page='users:login'), name='logout'),

    # User Profile URL
    path('profile/', user_profile, name='profile'),

    # User Dashboard URL
    path('dashboard/', user_dashboard, name='dashboard'),

    # User Update Profile URL
    path('update-profile/', update_user_profile, name='update_profile'),

    # Vendor Profile URL
    path('vendors/profile/', vendor_profile, name='vendor_profile'),

    # Vendor Dashboard URL
    path('vendors/dashboard/', vendor_dashboard, name='vendor_dashboard'),

    # Vendor Update Profile URL
    path('vendors/update-profile/', update_vendor_profile, name='update_vendor_profile'),
]