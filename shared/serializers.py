from rest_framework import serializers
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
    MenuItemImage,
    CartItem,
    PriceTier,
    AddOn,
    MenuItemPriceTier,
    Role,
    RolePermission
)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class TipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tip
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class StaffReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffReport
        fields = '__all__'

class ServerSwapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerSwap
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class IncentiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incentive
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class WaiterBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiterBadge
        fields = '__all__'

class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class TakeoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Takeout
        fields = '__all__'


class MenuItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemImage
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
     class Meta:
         model = CartItem
         fields = '__all__'
         
class PriceTierSerializer(serializers.ModelSerializer):
     class Meta:
         model = PriceTier
         fields = '__all__'
         
class AddOnSerializer(serializers.ModelSerializer):
     class Meta:
         model = AddOn
         fields = '__all__'

class MenuItemPriceTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemPriceTier
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'