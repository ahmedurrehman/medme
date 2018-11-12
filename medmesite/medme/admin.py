from django.contrib import admin

# Register your models here.
from medme.models import Order, Customer, Medicine, Drug, Composition, Company, Form, OrderItems


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    model = Order

    def order_items(self, obj):
        return "\n".join([str(item.name)+", " for item in obj.items.all()])


    def order_user(self, obj):
        return obj.customer.name
    order_user.short_description = 'Customer Name'

    list_display = ('orderNumber', 'order_user','order_items', 'status', 'totalBill', 'created')
    list_filter = ('status', 'created')
    search_fields = ('orderNumber', 'order_user')


class MedicineAdmin(admin.ModelAdmin):
    model = Medicine

    def company_name(self, obj):
        return obj.company.name

    company_name.short_description = 'Company'

    def form_name(self, obj):
        return obj.form.form

    form_name.short_description = 'Form'

    def get_compositions(self, obj):
        return "\n".join([str(c) for c in obj.composition.all()])

    get_compositions.short_description = 'Compositions'

    list_display = ('name', 'company_name', 'form_name', 'price', 'get_compositions', 'created')
    # list_filter = ('name', 'company')
    # search_fields = ('name', 'generic_name', 'company')


class DrugAdmin(admin.ModelAdmin):
    model = Drug
    list_display = ('name', 'created')


class CompositionAdmin(admin.ModelAdmin):
    model = Composition

    def drug_name(self, obj):
        return obj.drug.name

    drug_name.short_description = 'Drug'
    list_display = ('drug_name', 'potency')


admin.site.register(Customer, CustomerAdmin);
admin.site.register(Order, OrderAdmin);
admin.site.register(Medicine, MedicineAdmin);
admin.site.register(Drug, DrugAdmin);
admin.site.register(Composition, CompositionAdmin);
admin.site.register(Company);
admin.site.register(Form);
admin.site.register(OrderItems);
