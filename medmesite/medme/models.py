from django.db import models


# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=100)
    address = models.TextField(max_length=100, default='')
    extra = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('created', 'name')


class Company(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Drug(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Composition(models.Model):
    medicine = models.ForeignKey('Medicine', on_delete=models.DO_NOTHING, blank=True, null=True)
    drug = models.ForeignKey(Drug, on_delete=models.DO_NOTHING, blank=True, null=True)
    potency = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.drug.name + "-" + self.potency


class Form(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    form = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.form


class Medicine(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, related_name='medicines', on_delete=models.DO_NOTHING, blank=False)
    form = models.ForeignKey(Form, related_name='medicines', on_delete=models.DO_NOTHING, blank=False)
    price = models.IntegerField(default=0)
    drugs = models.ManyToManyField(Drug, related_name='drugs', through=Composition)

    def __str__(self):  # __unicode__ on Python 2
        return self.name + '(' + self.form.form + ')' + "-" + self.company.name

    def display_compositions(self):  # __unicode__ on Python 2
        return "\n".join([str(c) for c in Composition.objects.filter(medicine__id=self.id)])

    display_compositions.short_description = 'Compositions'

    class Meta:
        ordering = ('name', 'created',)


class Order(models.Model):
    STATUS_CHOICES = (
        ("NOT_CONFIRMED", "Not Confirmed"),
        ("IN_PROGRESS", "In Progress"),
        ("DELIVERED", "Delivered"),
        ("COMPLETED", "Completed"))

    orderNumber = models.AutoField(primary_key=True, auto_created=True)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, blank=False)
    address = models.TextField(default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_CONFIRMED')
    productCharges = models.IntegerField(default=0)
    deliveryCharges = models.IntegerField(default=0)
    extraCharges = models.IntegerField(default=0)
    totalBill = models.IntegerField(default=0)
    paymentReceived = models.IntegerField(default=0)
    items = models.ManyToManyField(Medicine, related_name='items', through='OrderItems')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return str(self.orderNumber) + "-" + self.customer.name

    def display_order_items(self):  # __unicode__ on Python 2
        return "\n".join([str(oi) for oi in OrderItems.objects.filter(order__orderNumber=self.orderNumber)])

    display_order_items.short_description = 'Items'


class Meta:
    ordering = ('created',)


class OrderItems(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # __unicode__ on Python 2
        return str(self.medicine.name) + "-" + str(self.quantity)

    class Meta:
        ordering = ('created',)
