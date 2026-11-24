from django.contrib import admin
from .models import Product, ProductImage, Order, OrderItem, DeliveryCost
from django.utils.html import mark_safe


# --- Product Image Inline with image preview and order field --- #
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview']
    ordering = ['id']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;" />')
        return "-"
    image_preview.short_description = "Preview"


# --- Product Admin with inline images --- #
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'stock']
    list_filter = ['available', 'category']
    search_fields = ['name', 'category']
    inlines = [ProductImageInline]


# --- Order Item Inline (readonly) --- #
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_order_time', 'name']
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj):
        return False


# --- Order Admin – editable only status --- #
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'total_amount', 'status', 'date']
    list_filter = ['status', 'date']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    readonly_fields = [
        'user', 'first_name', 'last_name', 'email',
        'address_1', 'address_2', 'zip_code', 'city',
        'phone', 'total_amount', 'date'
    ]
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        return [
            'status',
            'user', 'first_name', 'last_name', 'email',
            'address_1', 'address_2', 'zip_code', 'city',
            'phone', 'total_amount', 'date'
        ]


# --- Delivery Cost – only one record --- #
@admin.register(DeliveryCost)
class DeliveryCostAdmin(admin.ModelAdmin):
    list_display = ['total']

    def has_add_permission(self, request):
        return not DeliveryCost.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False