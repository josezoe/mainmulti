from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Vendor, Country, State, City, Timezone, AppModule, AppModulePermission, Role, UserRole
from .forms import CustomUserAdminForm, CustomUserCreationForm, AdminVendorForm, RoleForm, UserRoleForm, AppModuleForm

# Custom User admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'phone', 'country', 'state', 'city', 'preferred_currency', 'preferred_timezone', 'age', 'gender', 'income_level', 'housing_status', 'postal_code', 'lifestyle')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'password1', 'password2', 'phone', 'country'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# Vendor admin
@admin.register(Vendor)
class VendorAdmin(CustomUserAdmin):
    form = AdminVendorForm
    list_display = ('username', 'email', 'company_name', 'is_vendor_superuser')
    fieldsets = CustomUserAdmin.fieldsets + (
        ('Vendor Details', {
            'fields': ('company_name', 'tax_id', 'contact_person_name', 'phone_number', 'business_email', 'website', 'address_line1', 'address_line2', 'direction', 'menu', 'cuisine_type', 'cuisines', 'opening_hours', 'description', 'about', 'facilities', 'atmosphere', 'spoken_languages', 'payment_options', 'special_conditions')
        }),
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        ('Vendor Details', {
            'classes': ('collapse',),
            'fields': ('company_name', 'contact_person_name', 'phone_number', 'business_email', 'website', 'address_line1', 'address_line2')
        }),
    )

# App Module admin
class AppModulePermissionInline(admin.TabularInline):
    model = AppModulePermission
    extra = 1

@admin.register(AppModule)
class AppModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'app_label', 'is_full_app')
    search_fields = ['name', 'app_label']
    list_filter = ['is_full_app']
    inlines = [AppModulePermissionInline]
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "permissions":
            kwargs["queryset"] = Permission.objects.order_by('content_type__app_label', 'codename')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Role admin
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    form = RoleForm
    list_display = ('name', 'description', 'vendor')
    list_filter = ('vendor',)
    search_fields = ['name', 'description']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "vendor":
            kwargs["queryset"] = Vendor.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# UserRole admin
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    form = UserRoleForm
    list_display = ('user', 'role', 'vendor')
    list_filter = ('vendor', 'role')
    search_fields = ['user__username', 'role__name', 'vendor__company_name']

# Registering other models
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Timezone)

# Un-registering Group to prevent confusion since we're using our own role system
#admin.site.register(Group)