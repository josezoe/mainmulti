from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group
from django.utils import timezone
from django.db.models import JSONField
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save 
from django.dispatch import receiver

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

INCOME_CHOICES = (
    ('Low', '< $25,000'),
    ('Medium', '$25,000 - $75,000'),
    ('High', '> $75,000'),
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
    preferred_currency = models.CharField(max_length=3, null=True, blank=True)
    preferred_timezone = models.ForeignKey(Timezone, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    income_level = models.CharField(max_length=20, choices=INCOME_CHOICES, null=True, blank=True)
    housing_status = models.CharField(max_length=50, choices=HOUSING_CHOICES, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    # Geo-Targeting
    geolocation = models.JSONField(null=True, blank=True) # For last known location

    # Behavioral Analytics
    last_page_visited = models.URLField(null=True, blank=True)
    visit_count = models.IntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)
    search_history = models.JSONField(null=True, blank=True)
    purchase_history = models.JSONField(null=True, blank=True)

    # RFM Metrics for Segmentation
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    purchase_count = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # User Segmentation
    segment = models.CharField(max_length=100, null=True, blank=True, 
                               help_text="User segment, e.g., 'Champions', 'New Customers'")

    # Psychographic Segmentation
    lifestyle = models.CharField(max_length=50, choices=LIFESTYLE_CHOICES, null=True, blank=True)
    interests = models.JSONField(null=True, blank=True)  # List of interests

    # Additional fields for targeting and analysis
    marketing_preferences = models.JSONField(null=True, blank=True)# Store preferences for marketing campaigns
    behavior_tags = models.JSONField(null=True, blank=True) # Store tags like 'High Engagement', 'Frequent Buyer'
    
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.user_type == 'vendor':
            vendor_group, created = Group.objects.get_or_create(name='vendor')
            self.groups.add(vendor_group)
        super().save(*args, **kwargs)

    def update_purchase(self, amount):
        # Update RFM metrics
        self.last_purchase_date = timezone.now()
        self.purchase_count += 1
        self.total_spent += amount
        self.save()

    def calculate_rfm_score(self):
        # Simplified RFM scoring
        now = timezone.now()
        recency_score = 5 - min((now - self.last_purchase_date).days // 30, 4) if self.last_purchase_date else 0
        frequency_score = min(self.purchase_count // 5, 5)
        monetary_score = min(int(self.total_spent // 100), 5)
        return {
            'recency': recency_score,
            'frequency': frequency_score,
            'monetary': monetary_score,
            'total_score': recency_score + frequency_score + monetary_score
        }

    def get_segment(self):
        rfm_score = self.calculate_rfm_score()
        total = rfm_score['total_score']
        
        if total > 12:
            return "Champions"
        elif 9 <= total <= 12:
            return "Loyal Customers"
        elif 6 <= total < 9:
            return "Potential Loyalists"
        elif 3 <= total < 6:
            return "New Customers"
        else:
            return "At Risk"

    def update_behavior_tag(self, tag):
        if not self.behavior_tags:
            self.behavior_tags = {'tags': []}
        if tag not in self.behavior_tags['tags']:
            self.behavior_tags['tags'].append(tag)
        self.save()

    def calculate_clv(self):
        # Simplified CLV calculation
        return self.total_spent * (1 + self.purchase_count)  # Assuming more purchases increase value

    def estimate_income_by_housing(self):
        housing_to_income = {
            'Owns House': 'High',
            'Owns Apartment': 'Medium',
            'Rents': 'Low',
            'Other': 'Medium',
        }
        return housing_to_income.get(self.housing_status, 'Unknown')

    def analyze_purchase_patterns(self):
        if not self.purchase_history:
            return 'Unknown'
        
        luxury_count = sum(1 for item in self.purchase_history if item.get('price', 0) > 1000)  # Example threshold
        discount_use = sum(1 for item in self.purchase_history if item.get('used_coupon', False))
        
        if luxury_count > 5:  # Arbitrary threshold for 'high income' behavior
            return 'High'
        elif discount_use > 20:  # Arbitrary threshold for 'low income' behavior
            return 'Low'
        else:
            return 'Medium'

    def estimate_income_by_lifestyle(self):
        lifestyle_income_indicators = {
            'Travel': {'luxury_travel': 'High', 'budget_travel': 'Medium'},
            'Sports': {'golf': 'High', 'running': 'Medium'},
        }
        
        if not self.interests:
            return 'Medium'
        
        income_level = 'Medium'  # Default to medium
        for interest, details in self.interests.items():
            for activity in lifestyle_income_indicators.get(interest, {}).keys():
                if activity in details.get('types', []):
                    if lifestyle_income_indicators[interest][activity] == 'High':
                        return 'High'
                    elif lifestyle_income_indicators[interest][activity] == 'Low':
                        return 'Low'
        return income_level

    def predict_income(self):
        # Simple voting system for income prediction
        housing_income = self.estimate_income_by_housing()
        purchase_income = self.analyze_purchase_patterns()
        lifestyle_income = self.estimate_income_by_lifestyle()

        # Count votes for each income level
        votes = {
            'Low': 0,
            'Medium': 0,
            'High': 0,
            'Unknown': 0
        }
        
        for income in [housing_income, purchase_income, lifestyle_income]:
            if income in votes:
                votes[income] += 1

        # Determine the income level with the most votes
        predicted_income = max(votes, key=votes.get)
        
        # If there's a tie or if 'Unknown' has the highest vote, revert to a default or previous known income
        if votes[predicted_income] == 0 or (predicted_income == 'Unknown' and votes['Unknown'] == max(votes.values())):
            predicted_income = self.income_level or 'Medium'  # Use existing income_level if available, else default to 'Medium'
        
        return predicted_income

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
    vendor_unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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

    # Flag to indicate this user is a superuser for their own vendor operations
    is_vendor_superuser = models.BooleanField(default=False, help_text="Designates whether the user is a superuser for their vendor.")
    
    objects = VendorManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super(Vendor, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name
    
    def get_establishment_slug(self):
        return slugify(self.company_name)
    
    def has_perm(self, perm, obj=None):
        # Vendor superusers have all permissions related to their vendor's apps
        if perm.startswith('waiter_management.') or perm.startswith('vendor.'):
            return self.is_vendor_superuser
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        # Vendor superusers have all permissions in waiter_management and vendor apps
        if app_label in ['waiter_management', 'vendor']:
            return self.is_vendor_superuser
        return super().has_module_perms(app_label)

    def update_purchase(self, amount):
        # Update RFM metrics
        self.last_purchase_date = timezone.now()
        self.purchase_count += 1
        self.total_spent += amount
        self.save()


class RoleManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='role_manager')
    can_add_roles = models.BooleanField(default=False)
    can_edit_roles = models.BooleanField(default=False)
    can_delete_roles = models.BooleanField(default=False)

    def __str__(self):
        return f"Role Manager for {self.user.username}"

    class Meta:
        verbose_name = "Role Manager"
        verbose_name_plural = "Role Managers"

# Signal functions for RoleManager
@receiver(post_save, sender=CustomUser)
def create_role_manager(sender, instance, created, **kwargs):
    if created and instance.user_type == 'vendor':
        RoleManager.objects.create(user=instance, can_add_roles=True)

@receiver(post_save, sender=CustomUser)
def save_role_manager(sender, instance, **kwargs):
    if hasattr(instance, 'role_manager'):
        instance.role_manager.save()


#compliance 

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

class UserConsent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    consent_type = models.ForeignKey('ConsentType', on_delete=models.CASCADE)
    consented = models.BooleanField(default=False)
    date_consented = models.DateTimeField(null=True, blank=True)
    date_withdrawn = models.DateTimeField(null=True, blank=True)

class ConsentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)


