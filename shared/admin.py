from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
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
  
    AppModule,
    Notification
)

# Admin site header modification
admin.site.site_header = "Restaurant App Administration"
admin.site.index_title = "Data Management"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'category')
    search_fields = ('name', 'category')
    list_filter = ('is_available', 'category')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'status', 'vendor')
    list_filter = ('status', 'vendor')
    search_fields = ('number',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name','vendor', 'slug')
    search_fields = ('name','vendor__establishment_name')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'price', 'is_available', 'category')
    list_filter = ('menu', 'is_available', 'category')
    search_fields = ('name', 'description','category')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at', )
    search_fields = ('user__username', )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','product', 'quantity')
    list_filter = ('cart','product')
    search_fields = ('cart__user__username','product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','menu_item', 'quantity', 'price')
    list_filter = ('order','menu_item')
    search_fields = ('order__id','menu_item__name')

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'waiter', 'tip_time')
    list_filter = ('payment_method', 'tip_time')
    search_fields = ('order__id','waiter__username')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'reason')
    search_fields = ('order__id','reason')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'get_method_display_text', 'amount', 'payment_status', 'get_payment_time')
    list_filter = ('payment_status',)
    search_fields = ('order__id', )

    def get_method_display_text(self, obj):
        return obj.get_method_display()

    def get_payment_time(self, obj):
        return obj.get_payment_time()


# ... (previous code)



@admin.register(StaffReport)
class StaffReportAdmin(admin.ModelAdmin):
    list_display = ('waiter', 'start_time', 'end_time', 'total_sales')
    list_filter = ('start_time', 'end_time')
    search_fields = ('waiter__username',)

@admin.register(ServerSwap)
class ServerSwapAdmin(admin.ModelAdmin):
    list_display = ('original_waiter', 'new_waiter', 'table', 'order', 'swap_time')
    list_filter = ('swap_time', )
    search_fields = ('original_waiter__username', 'new_waiter__username')

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('sender__username', 'recipient__username')

@admin.register(Incentive)
class IncentiveAdmin(admin.ModelAdmin):
    list_display = ('waiter', 'amount', 'reason', 'date_given', 'is_active')
    list_filter = ('is_active', 'date_given')
    search_fields = ('waiter__username', 'reason')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_type', 'criteria', 'expiration_period')
    list_filter = ('badge_type',)
    search_fields = ('name', 'description','badge_type')

@admin.register(WaiterBadge)
class WaiterBadgeAdmin(admin.ModelAdmin):
    list_display = ('waiter', 'badge', 'date_awarded', 'expiration_date')
    list_filter = ('date_awarded','expiration_date')
    search_fields = ('waiter__username','badge__name')

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'amount', 'is_percentage')
    search_fields = ('order__id','name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('waiter', 'rating', 'review_time', 'order')
    list_filter = ('rating','review_time')
    search_fields = ('waiter__username', 'order__id')

@admin.register(Takeout)
class TakeoutAdmin(admin.ModelAdmin):
    list_display = ('order', 'pickup_time', 'delivery_option', 'is_picked_up')
    list_filter = ('is_picked_up', 'delivery_option')
    search_fields = ('order__id', )

@admin.register(MenuItemImage)
class MenuItemImageAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'image', 'description')
    search_fields = ('menu_item__name','description')

@admin.register(PriceTier)
class PriceTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(MenuItemPriceTier)
class MenuItemPriceTierAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'tier','price')
    list_filter = ('tier',)
    search_fields = ('menu_item__name','tier__name')







# Unregister the default Group model if you don't need it
admin.site.unregister(Group)

# Optionally, register Notification if it has admin-specific configurations
from django.contrib import admin
from .models import Notification  # Assuming Notification is in the same directory

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    def notification_type(self, obj):
        return obj.get_notification_type_display()
    
    notification_type.short_description = 'Notification Type'

    list_display = ('user', 'message', 'notification_type', 'created_at')
    list_filter = ('created_at',)  # Use a tuple with a trailing comma for a single item
    search_fields = ('user__username', 'message')