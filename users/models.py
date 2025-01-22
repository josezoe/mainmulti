from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group
from django.utils import timezone
from django.db.models import JSONField
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import Permission
from django.conf import settings
import os
import csv
from ipware import get_client_ip
from shared.geodata import get_city_data

# Constants for choices
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

LIFESTYLE_CHOICES = (
    ('Active', 'Active Lifestyle'),
    ('Sedentary', 'Sedentary Lifestyle'),
    ('Balanced', 'Balanced Lifestyle'),
)

INTEREST_CHOICES = (
    ('Sports', 'Sports'),
    ('Technology', 'Technology'),
    ('Art', 'Art'),
    ('Travel', 'Travel'),
    ('Food', 'Food'),
)  # Expand this list based on your needs

DEVICE_TYPE_CHOICES = (
    ('Mobile', 'Mobile Device'),
    ('Desktop', 'Desktop'),
    ('Tablet', 'Tablet'),
)

HOUSING_CHOICES = (
    ('Owns House', 'Owns House'),
    ('Owns Apartment', 'Owns Apartment'),
    ('Rents', 'Rents'),
    ('Other', 'Other'),
)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    currency = models.CharField(max_length=3)  # e.g., USD, INR
    default_timezone = models.CharField(max_length=100, help_text="Default timezone for this country")
    
    def __str__(self):
        return self.name

class Timezone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    name = models.CharField(max_length=100)
    timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE, related_name='states')
    
    def __str__(self):
        return f"{self.name}, {self.country}"

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}, {self.state}"

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='taxes')
    
    def __str__(self):
        return f"{self.name} - {self.percentage}%"
    

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)
    
    def __str__(self):
        return self.code
    
class HousingChoice(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} in {self.country.name}"

class HousingCost(models.Model):
    housing_choice = models.ForeignKey(HousingChoice, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    average_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cost_range_min = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cost_range_max = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.housing_choice.name} cost in {self.currency.code}"
    
class IncomeChoice(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    min_threshold = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    max_threshold = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} in {self.currency.code} ({self.country.name})"

    class Meta:
        unique_together = ('country', 'currency', 'name')

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    unique_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    preferred_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_timezone = models.ForeignKey(Timezone, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    housing_status = models.ForeignKey(HousingChoice, on_delete=models.SET_NULL, null=True, blank=True)
    income_level = models.ForeignKey(IncomeChoice, on_delete=models.SET_NULL, null=True, blank=True)

    # Geo-Targeting - Added IP tracking
    last_known_ip = models.GenericIPAddressField(null=True, blank=True)
    geolocation = models.JSONField(null=True, blank=True) # For last known location

    # Behavioral Analytics
    last_page_visited = models.URLField(null=True, blank=True)
    visit_count = models.IntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)
    purchase_history = models.JSONField(null=True, blank=True)

    # RFM Metrics for Segmentation
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    purchase_count = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # User Segmentation
    segment = models.CharField(max_length=100, null=True, blank=True, 
                               help_text="User segment, e.g., 'Champions', 'New Customers'")

    # Psychographic Segmentation - Denormalized for performance
    lifestyle = models.CharField(max_length=50, choices=LIFESTYLE_CHOICES, null=True, blank=True)

    # Additional fields for targeting and analysis
    marketing_preferences = models.JSONField(null=True, blank=True)# Store preferences for marketing campaigns
    behavior_tags = models.JSONField(null=True, blank=True) # Store tags like 'High Engagement', 'Frequent Buyer'
    
    objects = CustomUserManager()

    def update_geo_info(self, ip):
        """
        Update user's currency and timezone based on their IP address using CSV data.
        """
        try:
            geoname_id = self.get_geoname_id_from_ip(ip)  # You need to implement this method
            city_info = get_city_data(geoname_id)
            
            if city_info:
                country_code = city_info.get('country_iso_code')
                timezone_name = city_info.get('time_zone')
                
                if country_code:
                    country, created = Country.objects.get_or_create(code=country_code)
                    currency, created = Currency.objects.get_or_create(code=country.currency)
                    self.preferred_currency = currency
                
                if timezone_name:
                    timezone_obj, created = Timezone.objects.get_or_create(name=timezone_name)
                    self.preferred_timezone = timezone_obj
                
                self.last_known_ip = ip
                self.save()
                return True
            else:
                print(f"No location data found for IP: {ip}")
                return False
        except Exception as e:
            print(f"Error updating geo info: {e}")
            return False

    def save(self, *args, **kwargs):
        if self.last_known_ip and self.last_known_ip != self.get_client_ip():
            self.update_geo_info(self.get_client_ip())
        super().save(*args, **kwargs)

    def get_client_ip(self):
        # Implement this method to fetch the current client's IP address
        from ipware import get_client_ip
        ip, _ = get_client_ip(self.request)  # 'self.request' needs to be set in your views or middleware
        return ip

    def get_geoname_id_from_ip(self, ip):
        blocks_csv_path = os.path.join(settings.BASE_DIR, 'shared', 'Geocity', 'blocks.csv')  # Assuming you have this CSV
        with open(blocks_csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.ip_in_range(ip, row['network']):
                    return row['geoname_id']
        return None

    def ip_in_range(self, ip, network):
        import ipaddress
        return ipaddress.ip_address(ip) in ipaddress.ip_network(network)


class UserDevice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    browser = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.device_type}"

class JourneyStage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField()  # To define the sequence in the journey

    def __str__(self):
        return self.name

class UserJourney(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stage = models.ForeignKey(JourneyStage, on_delete=models.CASCADE)
    date_entered = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'stage')

    def __str__(self):
        return f"{self.user.username} - {self.stage.name}"

class VendorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='vendor')

    def create_vendor(self, username, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'vendor')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

class Vendor(CustomUser):
    # Basic Information
    company_name = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=20, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    can_manage_roles = models.BooleanField(default=False, help_text="Can manage roles for this vendor")
    is_vendor_superuser = models.BooleanField(default=False)
    # Contact Information
    contact_person_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    # Address and Directions
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    direction = models.TextField(null=True, blank=True)

    # Menu and Cuisine
    menu = models.URLField(null=True, blank=True)  # Assuming menu is hosted externally or uploaded elsewhere
    cuisine_type = models.CharField(max_length=100, null=True, blank=True)  # E.g., Italian, Indian
    cuisines = models.TextField(null=True, blank=True)  # For listing multiple cuisines

    # Operational Information
    opening_hours = models.TextField(null=True, blank=True)  # Format like "Mon-Sat: 9am-9pm, Sun: Closed"
    description = models.TextField(null=True, blank=True)

    # Additional Information
    about = models.TextField(null=True, blank=True)
    facilities = models.TextField(null=True, blank=True)  # E.g., "Wi-Fi, Parking, Outdoor Seating"
    atmosphere = models.CharField(max_length=255, null=True, blank=True)  # E.g., "Casual, Romantic"
    spoken_languages = models.CharField(max_length=255, null=True, blank=True)
    payment_options = models.CharField(max_length=255, null=True, blank=True)  # E.g., "Cash, Credit Cards, PayPal"
    special_conditions = models.TextField(null=True, blank=True)  # E.g., Dress code, age restrictions

    # Review System (simplified; you might want a separate Review model)
    average_rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VendorManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name
    
    def get_establishment_slug(self):
        return slugify(self.company_name)

class AppModule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app_label = models.CharField(max_length=100)
    is_full_app = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class AppModulePermission(models.Model):
    module = models.ForeignKey(AppModule, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.module.name} - {self.permission.name}"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='roles')

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='user_roles')

    class Meta:
        unique_together = ('user', 'role', 'vendor')  # One role per user per vendor

    def __str__(self):
        return f"{self.user.username} - {self.role.name} at {self.vendor.company_name}"

# Privacy and compliance models

class UserPrivacySettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    can_sell_data = models.BooleanField(default=False)
    can_target_ads = models.BooleanField(default=False)
    can_share_data = models.BooleanField(default=False)

class PrivacyByDesign(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    privacy_notice_accepted = models.BooleanField(default=False)
    data_minimized = models.JSONField(null=True, blank=True)  # Assuming JSON data for minimized fields

class IndianUserData(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    consent_for_processing = models.BooleanField(default=False)
    data_purpose = models.TextField(blank=True, null=True)
    data_lifecycle = models.JSONField(null=True, blank=True)

class GDPRCompliance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    has_access_right = models.BooleanField(default=False)
    has_rectification_right = models.BooleanField(default=False)
    has_erase_right = models.BooleanField(default=False)
    has_portability_right = models.BooleanField(default=False)

class ConsentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class UserConsent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    consent_type = models.ForeignKey(ConsentType, on_delete=models.CASCADE)
    consented = models.BooleanField(default=False)
    date_consented = models.DateTimeField(null=True, blank=True)
    date_withdrawn = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.consent_type.name} - {'Consented' if self.consented else 'Not Consented'}"

# Helper function for location-based compliance
def get_user_location(request):
    """Get user's location based on IP address."""
    ip, _ = get_client_ip(request)
    if ip:
        # Note: You'll need to implement or integrate a GeoIP service here
        # Example:
        # from django.contrib.gis.geoip2 import GeoIP2
        # g = GeoIP2()
        # return g.city(ip)
        return {'country'}