from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Vendor, Country, State, City, Timezone, Role, UserRole, AppModule
from .forms import VendorSignupForm, VendorProfileForm, VendorUpdateForm, UserSignupForm, UserProfileForm
from shared.models import Notification 
from shared.services import create_notification
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .serializers import CustomUserSerializer, VendorSerializer, CountrySerializer, StateSerializer, CitySerializer, TimezoneSerializer, RoleSerializer, UserRoleSerializer, AppModuleSerializer
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
# Vendor Signup
class VendorSignupView(View):
    template_name = 'users/vendor_signup.html'
    form_class = VendorSignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if Vendor.objects.count() == 0:
                user.is_superuser = True
                user.is_staff = True
            user.save()
            temp_password = get_random_string(length=10)
            user.set_password(temp_password)
            user.save()

            send_mail(
                subject='Your Temporary Password',
                message=f'Your temporary password is: {temp_password}. Please change it upon first login.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            create_notification(user, 'Your vendor account is now active. Please change your temporary password.', 'success')
            
            user = authenticate(username=user.username, password=temp_password)
            login(request, user)
            messages.success(request, _('Vendor account created successfully!'))
            return redirect('users:vendor_dashboard')  # Redirect to vendor dashboard
        return render(request, self.template_name, {'form': form})

# Vendor Profile
class VendorProfileView(LoginRequiredMixin, View):
    template_name = 'users/vendor_profile.html'
    form_class = VendorProfileForm

    def get(self, request):
        if request.user.user_type != 'vendor':
            raise PermissionDenied
        form = self.form_class(instance=request.user)
        unread_notifications_count = Notification.objects.filter(user=request.user, read=False).count()
        return render(request, self.template_name, {'form': form, 'unread_notifications_count': unread_notifications_count})

    def post(self, request):
        if request.user.user_type != 'vendor':
            raise PermissionDenied
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully!'))
            create_notification(request.user, 'Your profile has been updated.', 'success')
        return render(request, self.template_name, {'form': form})

# Vendor Dashboard
class VendorDashboardView(LoginRequiredMixin, View):
    template_name = 'users/vendor_dashboard.html'

    def get(self, request):
        if request.user.user_type != 'vendor':
            raise PermissionDenied
        
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        
        context = {
            'user': request.user,
            'notifications': notifications,
        }

        return render(request, self.template_name, context)

# Adding Users with Specific Permissions
class AddUserView(LoginRequiredMixin, View):
    template_name = 'users/add_user.html'
    
    def get(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'vendor'  
            
            # Set location
            country = request.POST.get('country')
            state = request.POST.get('state')
            city = request.POST.get('city')
            
            if country:
                country_obj = get_object_or_404(Country, name=country)
                user.country = country_obj
            if state:
                state_obj = get_object_or_404(State, name=state, country=country_obj)
                user.state = state_obj
            if city:
                city_obj = get_object_or_404(City, name=city, state=state_obj)
                user.city = city_obj

            temp_password = get_random_string(length=10)
            user.set_password(temp_password)
            user.save()

            # Vendor-based permissions
            model_permissions = request.POST.getlist('model_permissions')
            for model_name in model_permissions:
                model = ContentType.objects.get(model=model_name.lower()).model_class()
                permissions = Permission.objects.filter(content_type__model=model_name.lower())
                user.user_permissions.add(*permissions)

            # Location-based permissions
            location_group_name = f"{country_obj.name}_{state_obj.name}" if state_obj else country_obj.name
            location_group, created = Group.objects.get_or_create(name=location_group_name)
            user.groups.add(location_group)

            send_mail(
                subject='Your Temporary Password',
                message=f'Your temporary password is: {temp_password}. Please change it upon first login.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            create_notification(user, 'Your vendor account has been created. Use the temporary password to login.', 'success')
            create_notification(request.user, f'New vendor {user.username} added.', 'info')

            messages.success(request, _('User added successfully with temporary password!'))
            return redirect('users:vendor_dashboard')
        return render(request, self.template_name, {'form': form})

# Vendor Home
class VendorHomeView(LoginRequiredMixin, View):
    template_name = 'users/vendor_home.html'

    def get(self, request):
        if request.user.user_type != 'vendor':
            raise PermissionDenied
        return render(request, self.template_name, {'user': request.user})

# Change Password for Vendors
class VendorChangePasswordView(LoginRequiredMixin, View):
    template_name = 'users/change_password.html'
    form_class = PasswordChangeForm

    def get(self, request):
        if request.user.user_type != 'vendor':
            raise PermissionDenied
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.user_type != 'vendor':
            raise PermissionDenied
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after changing password
            messages.success(request, _('Your password was successfully updated!'))
            create_notification(request.user, 'Your password has been changed.', 'success')
            return redirect('users:vendor_dashboard')
        return render(request, self.template_name, {'form': form})

# User Signup
class UserSignupView(View):
    template_name = 'users/signup.html'
    form_class = UserSignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Account created successfully!'))
            return redirect('users:user_dashboard')  # Redirect to user dashboard
        return render(request, self.template_name, {'form': form})

# User Profile
@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile')  # Redirect to a success page
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/user_profile.html', {'form': form})

# User Dashboard
@login_required
def user_dashboard(request):
    context = {
        'user': request.user,
        # Add more context as needed
    }
    return render(request, 'users/dashboard.html', context)

# Update User Profile
@login_required
def update_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profile updated successfully!'))
            return redirect('users:user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})

# Vendor Profile View
@login_required
def vendor_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            # Here you might want to add a success message or redirect
            return render(request, 'users/vendor_profile.html', {'form': form})
    else:
        form = VendorProfileForm(instance=vendor)

    return render(request, 'users/vendor_profile.html', {'form': form})

# Vendor Dashboard View
@login_required
def vendor_dashboard(request):
    if not isinstance(request.user, Vendor):
        raise PermissionDenied("You do not have permission to access this page.")

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'notifications': notifications,
        # Add other data as needed
    }
    
    return render(request, 'users/vendor_dashboard.html', context)

# Update Vendor Profile
@login_required
def update_vendor_profile(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('users:vendor_profile')  # Assuming this is the name of the profile view
    else:
        form = VendorProfileForm(instance=vendor)

    return render(request, 'users/update_vendor_profile.html', {'form': form})

# API Views

class CustomAuthToken(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.unique_id,
            'user_type': user.user_type,
        })

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('users:user_dashboard')  


# Generic API Views for models
class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CountryDetail(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class StateList(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class StateDetail(generics.RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CityDetail(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class TimezoneList(generics.ListAPIView):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]

class TimezoneDetail(generics.RetrieveAPIView):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]

class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class CustomUserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class VendorList(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

class VendorDetail(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

class RoleList(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

class RoleDetail(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

class UserRoleList(generics.ListAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

class UserRoleDetail(generics.RetrieveAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]

class AppModuleList(generics.ListAPIView):
    queryset = AppModule.objects.all()
    serializer_class = AppModuleSerializer
    permission_classes = [IsAuthenticated]

class AppModuleDetail(generics.RetrieveAPIView):
    queryset = AppModule.objects.all()
    serializer_class = AppModuleSerializer
    permission_classes = [IsAuthenticated]