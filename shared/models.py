from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from users.models import Vendor, CustomUser as User
from django.contrib.auth.models import Permission
import random


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., Pizza, Burger, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
'''class Waiter(AbstractUser):
    """
    Custom waiter model extending Django's User model for authentication.
    
    This model includes:
    - Basic user authentication fields from AbstractUser
    - Vendor association
    - Detailed employment information
    - Performance metrics
    - Operational preferences and restrictions
    - Availability and scheduling
    - Tip management
    - Badge system
    - Efficiency metrics
    """

    # Employment Information
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='waiters')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    position = models.CharField(max_length=50, choices=[
        ('WAITER', 'Waiter'),
        ('HEAD_WAITER', 'Head Waiter'),
        ('SERVER', 'Server'),
        ('BARISTA', 'Barista'),
        ('HOST', 'Host/Hostess'),
        ('MANAGER', 'Manager'),
    ], default='WAITER')
    current_status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ON_LEAVE', 'On Leave'),
        ('TERMINATED', 'Terminated'),
    ], default='ACTIVE')
    
    # Contact Information
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    
    # Performance Metrics
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_rating = models.FloatField(null=True, blank=True)
    reviews = models.IntegerField(default=0)
    tables_served = models.IntegerField(default=0)
    orders_completed = models.IntegerField(default=0)
    
    # Tip Management
    total_tips = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tip_percentage = models.FloatField(default=0.0, help_text="Average tip percentage")

    # Operational Preferences
    preferred_station = models.CharField(max_length=100, null=True, blank=True, help_text="Preferred section or area")
    shift_preference = models.CharField(max_length=200, null=True, blank=True, help_text="Preferred shift times")
    uniform_size = models.CharField(max_length=20, null=True, blank=True)
    language_spoken = models.CharField(max_length=200, null=True, blank=True, help_text="Languages spoken")
    skill_level = models.CharField(max_length=50, choices=[
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    ], default='BEGINNER')
    
    # Availability and Scheduling
    is_available = models.BooleanField(default=True, help_text="Indicates if the waiter is currently available for shifts")
    availability_schedule = models.JSONField(null=True, blank=True, help_text="JSON representation of availability")
    
    # Certifications or Special Training
    certifications = models.TextField(null=True, blank=True, help_text="List of certifications or special training")

    # Efficiency Metrics
    average_service_time = models.DurationField(null=True, blank=True, help_text="Average time to serve an order")
    table_turnover_rate = models.FloatField(null=True, blank=True, help_text="Average tables turned per hour of work")
    order_accuracy_rate = models.FloatField(null=True, blank=True, help_text="Percentage of orders served correctly")
    upsell_rate = models.FloatField(null=True, blank=True, help_text="Rate of upselling items")

    # Custom User Fields
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'employee_id', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Waiter'
        verbose_name_plural = 'Waiters'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.employee_id}"

    def get_sales_this_month(self):
        """Calculate total sales for this month by this waiter."""
        sales = OrderItem.objects.filter(
            order__waiter=self,
            order__order_time__year=timezone.now().year,
            order__order_time__month=timezone.now().month
        ).aggregate(total=models.Sum('price'))['total'] or 0
        return sales

    def update_sales(self, amount):
        """Update the total sales for this waiter."""
        self.total_sales += amount
        self.save()

    def get_menu(self):
        """Return the menu associated with this waiter's vendor."""
        return Menu.objects.filter(vendor=self.vendor).first()

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_id = Waiter.objects.filter(vendor=self.vendor).aggregate(models.Max('employee_id'))['employee_id__max']
            if last_id:
                last_number = int(last_id[2:]) if last_id[2:].isdigit() else 0
                self.employee_id = f"W{self.vendor.id}{last_number + 1:03d}"
            else:
                self.employee_id = f"W{self.vendor.id}001"
        super(Waiter, self).save(*args, **kwargs)

    def update_performance(self, order_completed=True):
        """Update performance metrics when an order is completed or when server swaps occur."""
        if order_completed:
            self.tables_served += 1
            self.orders_completed += 1
        else:
            self.tables_served -= 1
            self.orders_completed -= 1
        self.save()

    def update_tips(self, tip_amount):
        """Update the total tips for this waiter."""
        self.total_tips += tip_amount
        if self.total_sales > 0:
            self.tip_percentage = (self.total_tips / self.total_sales) * 100
        self.save()

    def get_current_promotions(self):
        """Return active promotions for this waiter."""
        return Promotion.objects.filter(recipient=self, is_active=True, expiry__gte=timezone.now()) \
                                | Promotion.objects.filter(recipient=self, is_active=True, expiry__isnull=True)

    def add_incentive(self, amount, reason):
        """Add an incentive for this waiter."""
        Incentive.objects.create(waiter=self, amount=amount, reason=reason)

    def award_badge(self, badge_name):
        """Award a badge to this waiter."""
        badge = Badge.objects.get_or_create(name=badge_name)[0]
        if not WaiterBadge.objects.filter(waiter=self, badge=badge).exists():
            WaiterBadge.objects.create(waiter=self, badge=badge)

    def get_badges(self):
        """Return all badges awarded to this waiter."""
        return self.waiterbadge_set.all()

    def update_efficiency_metrics(self, order):
        """
        Update efficiency metrics based on the completion of an order.
        
        :param order: The Order instance that was completed
        """
        # Average Service Time
        if not self.average_service_time:
            self.average_service_time = order.time_to_completion
        else:
            # Simple moving average for service time
            self.average_service_time = (self.average_service_time + order.time_to_completion) / 2

        # Table Turnover Rate
        if self.tables_served > 0:
            # Assuming you track shift start and end times elsewhere
            hours_worked = (timezone.now() - self.shift_start_time).total_seconds() / 3600 if hasattr(self, 'shift_start_time') else 1
            self.table_turnover_rate = self.tables_served / hours_worked

        # Order Accuracy Rate
        # You would need to track errors, perhaps in another model or through staff feedback
        if hasattr(order, 'error_count'):
            total_orders = self.orders_completed + 1  # +1 for the current order
            correct_orders = total_orders - order.error_count
            self.order_accuracy_rate = (correct_orders / total_orders) * 100

        # Upsell Rate
        # Assuming you track upsells in another model or method
        if hasattr(self, 'total_upsells') and hasattr(self, 'total_orders'):
            self.upsell_rate = (self.total_upsells / self.total_orders) * 100

        self.save()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='waiter_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='waiter_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )'''


class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('FREE', 'Free'), ('OCCUPIED', 'Occupied')], default='FREE')

    def __str__(self):
        return f"Table {self.number}"
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def calculate_total_amount(self, tax_rate=0.1, commission_rate=0.05):
        """Calculate the total amount including tax and commission."""
        subtotal = self.cart.total_price()
        tax = subtotal * tax_rate
        commission = subtotal * commission_rate
        self.total_amount = subtotal + tax + commission
        self.save()
        return self.total_amount


class PriceTier(models.Model):
    name = models.CharField(max_length=50)  # e.g., 'Small', 'Large', 'Happy Hour'
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Menu(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, primary_key=True, related_name='vendor_menu')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            vendor_slug = self.vendor.get_establishment_slug()
            self.slug = f"{vendor_slug}/{slugify(self.name)}"
        super(Menu, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(null=True, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    add_ons = models.ManyToManyField('AddOn', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            menu_slug = self.menu.slug
            self.slug = f"{menu_slug}/{slugify(self.name)}"
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class AddOn(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class MenuItemPriceTier(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    tier = models.ForeignKey(PriceTier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='menu_item_images/')
    description = models.CharField(max_length=200, blank=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart {self.cart.id}"

    def total_price(self):
        return self.product.price * self.quantity


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order {self.order.id}"


class Tip(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tips')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tip_time = models.DateTimeField(default=timezone.now)
    waiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tips_received')
    payment_method = models.CharField(max_length=20, choices=[
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
    ], default='CASH')

    def __str__(self):
        return f"Tip of {self.amount} for Order {self.order.id} by {self.waiter.username}"


class Discount(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discounts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('ONLINE', 'Online Payment'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS,default='credit_card')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    payment_time = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ], default='PENDING')

    def __str__(self):
        return f"Payment for Order {self.order.id}: {self.total_amount}"

    def calculate_total_amount(self):
        """Calculate the total amount including tax and commission."""
        self.total_amount = self.amount + self.tax + self.commission
        self.save()
        return self.total_amount
    
    def get_method_display_text(self):
      return self.get_method_display()
    
    def get_payment_time(self):
        return self.payment_time

class SplitBill(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)


class StaffReport(models.Model):
    waiter = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comments = models.TextField(blank=True)

    def generate_report(self):
        """
        Generate a detailed report for this staff member's shift including tips.
        """
        self.total_sales = self.waiter.get_sales_this_month()
        self.total_tips = self.waiter.tips_received.aggregate(models.Sum('amount'))['amount__sum'] or 0
        self.save()


class ServerSwap(models.Model):
    original_waiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='original_swaps')
    new_waiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new_swaps')
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    swap_time = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=True, help_text="Reason for the swap")

    class Meta:
        unique_together = ('original_waiter', 'new_waiter', 'table', 'order')

    def __str__(self):
        if self.table:
            return f"Swap from {self.original_waiter.username} to {self.new_waiter.username} for Table {self.table.number}"
        elif self.order:
            return f"Swap from {self.original_waiter.username} to {self.new_waiter.username} for Order {self.order.id}"
        return f"Swap from {self.original_waiter.username} to {self.new_waiter.username}"

    def perform_swap(self):
        if self.table:
            self.table.status = 'OCCUPIED'
            self.table.save()
            for order in Order.objects.filter(table=self.table):
                order.waiter = self.new_waiter
                order.save()
        elif self.order:
            self.order.waiter = self.new_waiter
            self.order.save()

        self.original_waiter.update_performance(False)
        self.new_waiter.update_performance(True)


class Promotion(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_promotions')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_promotions')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Promotion from {self.sender.username} to {self.recipient.username}"


class Incentive(models.Model):
    waiter = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    date_given = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Incentive for {self.waiter.username} - {self.amount}"


class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/', blank=True, null=True)
    badge_type = models.CharField(max_length=50, choices=[
        ('SALES', 'Sales'),
        ('SERVICE', 'Service'),
        ('LOYALTY', 'Loyalty'),
        ('SPECIAL', 'Special Event')
    ], default='SALES')
    criteria = models.TextField(help_text="Criteria for earning this badge")
    expiration_period = models.DurationField(null=True, blank=True, help_text="Duration after which the badge expires")

    def __str__(self):
        return self.name


class WaiterBadge(models.Model):
    waiter = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_awarded = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.badge.name} awarded to {self.waiter.username}"

    def is_expired(self):
        if self.expiration_date:
            return timezone.now().date() > self.expiration_date
        return False

    def save(self, *args, **kwargs):
        if self.badge.expiration_period:
            self.expiration_date = self.date_awarded + timezone.timedelta(days=self.badge.expiration_period.days)
        super().save(*args, **kwargs)


class Tax(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='taxes')
    name = models.CharField(max_length=100)  # e.g., GST, VAT, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_percentage = models.BooleanField(default=False)  # If True, amount is a percentage

    def __str__(self):
        return f"Tax {self.name} of {self.amount}{'%' if self.is_percentage else 'USD'} on Order {self.order.id}"

    def get_amount(self):
        if self.is_percentage:
            return self.order.total_price * (self.amount / 100)
        return self.amount


class Review(models.Model):
    waiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],  # Ensures rating is between 1 and 5
        choices=[(i, i) for i in range(1, 6)]  # 1 to 5 stars
    )
    comment = models.TextField(blank=True, null=True)
    review_time = models.DateTimeField(default=timezone.now)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"Review for {self.waiter.username} - {self.rating} stars"


class Takeout(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='takeout')
    pickup_time = models.DateTimeField()
    is_picked_up = models.BooleanField(default=False)
    delivery_option = models.CharField(max_length=20, choices=[
        ('PICKUP', 'Pickup'),
        ('DELIVERY', 'Delivery'),
    ], default='PICKUP')
    delivery_address = models.TextField(blank=True, null=True)  # Only applicable for delivery

    def __str__(self):
        return f"Takeout for Order {self.order.id}"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.CharField(max_length=255)  # Can be replaced with a User FK if needed

    def __str__(self):
        return f"{self.action} on Order {self.order.id} by {self.performed_by}"


# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."


# Email Model
class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Email to {self.user.email}: {self.subject}"


# SMS Model
class SMS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"SMS to {self.user.username}: {self.message[:50]}..."


# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Cart {self.cart.id}"

    def total_price(self):
        return self.product.price * self.quantity


   

class AppModule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app_label = models.CharField(max_length=100, help_text="The app label this module belongs to (e.g., 'shared', 'users')")
    description = models.TextField(blank=True, null=True)
    is_full_app = models.BooleanField(default=False, help_text="Check if this represents the entire app")
    permissions = models.ManyToManyField(Permission, related_name='app_modules', blank=True)

    def __str__(self):
        return self.name

    def get_permissions(self):
        if self.is_full_app:
            return Permission.objects.filter(content_type__app_label=self.app_label)
        return self.permissions.all()

    class Meta:
        verbose_name = "App Module"
        verbose_name_plural = "App Modules"

    


class DummyPaymentGateway:
    @staticmethod
    def process_payment(amount):
        """
        Simulate a payment process for testing purposes.
        Returns True if payment is successful, False otherwise.
        """
        # Simulate a success rate of 90%
        return random.random() < 0.9

    @staticmethod
    def create_payment_intent(amount):
        """
        Simulate creation of a payment intent for testing purposes.
        """
        if random.random() < 0.9:  # 90% chance of success
            return "dummy_client_secret_" + str(random.randint(1000, 9999))
        return None

    @staticmethod
    def confirm_payment(payment_intent_id):
        """
        Simulate confirmation of a payment for testing purposes.
        """
        if random.random() < 0.9:  # 90% chance of success
            return {"status": "succeeded"}
        return {"status": "failed"}
    




