from django import forms
from .models import (
    Product,
    Table,
    Menu,
    MenuItem,
    Cart,
    Order,
    OrderItem,
    Tip,
    Discount,
    Payment,
    StaffReport,
    ServerSwap,
    Promotion,
    Incentive,
    Badge,
    WaiterBadge,
    Tax,
    Review,
    Takeout,
    CartItem,
    Role
)

# Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'is_available', 'category']


# Table Form
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'status', 'vendor']
        

# Menu Form
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description']

# MenuItem Form
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'menu',
            'name',
            'description',
            'price',
            'category',
            'image',
            'is_available',
            'stock_quantity',
            'meta_description',
            'meta_keywords',
            'add_ons',
        ]

# Cart Form (basic, might need more depending on use)
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # Fields are usually not needed, items are added via cart item forms

class CartItemForm(forms.ModelForm):
     class Meta:
        model = CartItem
        fields = ['product', 'quantity']


# Order Form (most likely to be created programmatically)
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item','quantity', 'special_instructions', 'price']

# Tip Form
class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['amount', 'payment_method']
        widgets = {
           'payment_method': forms.Select(choices=Tip.payment_method.field.choices)
        }


# Discount Form
class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['amount', 'reason']

# Payment Form
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method','amount', 'payment_method']
        widgets = {
           'method': forms.Select(choices=Payment.PAYMENT_METHODS),
        }

# StaffReport Form
class StaffReportForm(forms.ModelForm):
    class Meta:
        model = StaffReport
        fields = ['start_time', 'end_time', 'comments']


# ServerSwap Form
class ServerSwapForm(forms.ModelForm):
    class Meta:
        model = ServerSwap
        fields = ['original_waiter', 'new_waiter', 'table','order','reason']


# Promotion Form
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['recipient', 'message','expiry']

# Incentive Form
class IncentiveForm(forms.ModelForm):
    class Meta:
        model = Incentive
        fields = ['amount', 'reason']

# Badge Form
class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'image', 'badge_type','criteria','expiration_period']
        widgets = {
           'badge_type': forms.Select(choices=Badge.badge_type.field.choices)
        }


# WaiterBadge Form (Usually, awarded by the system)
class WaiterBadgeForm(forms.ModelForm):
    class Meta:
        model = WaiterBadge
        fields = ['badge']


# Tax Form
class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = ['name', 'amount','is_percentage']


# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


# Takeout Form
class TakeoutForm(forms.ModelForm):
    class Meta:
        model = Takeout
        fields = ['pickup_time', 'delivery_option', 'delivery_address']
        widgets = {
            'delivery_option': forms.Select(choices=Takeout.delivery_option.field.choices),
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description', 'vendor']