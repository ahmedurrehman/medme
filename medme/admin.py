from django.contrib import admin

# Register your models here.
from medme.models import Order, MedmeUser, Medicine


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    model = Order

    def order_user(self, obj):
        return obj.customer.name

    order_user.short_description = 'Customer Name'

    list_display = ('orderNumber', 'order_user', 'status', 'totalBill', 'created')
    list_filter = ('status', 'created')


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'company', 'doz', 'price', 'created')
    list_filter = ('generic_name', 'company')
    search_fields = ('name', 'generic_name', 'company')


admin.site.register(MedmeUser, UserAdmin);
admin.site.register(Order, OrderAdmin);
admin.site.register(Medicine, MedicineAdmin);
