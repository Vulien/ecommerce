
# Register your models here.
from django.contrib import admin
from .models import Product, Order, OrderItem

admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Không hiển thị các dòng trống thêm
    
def mark_as_processed(modeladmin, request, queryset):
    queryset.update(processed=True)
mark_as_processed.short_description = "Đánh dấu đơn hàng đã lên đơn"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'address', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('name', 'phone', 'email', 'address')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)  # Nếu bạn muốn khóa thời gian tạo đơn hàng

admin.site.register(Order, OrderAdmin)


