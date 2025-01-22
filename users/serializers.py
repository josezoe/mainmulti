from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import CustomUser, Vendor, Country, State, City, Timezone, AppModule, Role, UserRole, AppModulePermission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class AppModuleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = AppModule
        fields = ['id', 'name', 'app_label', 'is_full_app', 'permissions']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'vendor']

class UserRoleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Assuming you want to display username
    role = serializers.StringRelatedField()  # Assuming you want to display role name
    vendor = serializers.StringRelatedField()  # Assuming you want to display vendor name

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'vendor']

class CustomUserSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(many=True, read_only=True)
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'country', 'state', 'city', 'profile_image', 'preferred_currency', 'preferred_timezone', 'age', 'gender', 'postal_code', 'housing_status', 'income_level', 'user_type', 'roles']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # If you want to include specific permissions for this user:
        ret['permissions'] = [p.codename for p in instance.user_permissions.all()]
        return ret

class VendorSerializer(CustomUserSerializer):
    class Meta:
        model = Vendor
        fields = CustomUserSerializer.Meta.fields + ['company_name', 'tax_id', 'contact_person_name', 'phone_number', 'business_email', 'website', 'address_line1', 'address_line2', 'direction', 'menu', 'cuisine_type', 'cuisines', 'opening_hours', 'description', 'about', 'facilities', 'atmosphere', 'spoken_languages', 'payment_options', 'special_conditions', 'is_vendor_superuser']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Add any vendor-specific custom logic here if needed
        return ret

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'currency', 'default_timezone']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'country', 'timezone']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'state']

class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timezone
        fields = ['id', 'name']

class AppModulePermissionSerializer(serializers.ModelSerializer):
    module = AppModuleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)

    class Meta:
        model = AppModulePermission
        fields = ['id', 'module', 'permission']