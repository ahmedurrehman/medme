from django.db import models

# Create your models here.

class MedmeUser(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    address = models.TextField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        ordering = ('created', 'name')


class Medicine(models.Model):
    id = models.IntegerField(primary_key=True,auto_created=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    generic_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    doz = models.CharField(max_length=15, null=True)
    price = models.IntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.name + "-" + self.company

    class Meta:
        ordering = ('name', 'created',)


class Order(models.Model):

    STATUS_CHOICES = (
    ("NOT_CONFIRMED", "Not Confirmed"),
    ("IN_PROGRESS", "In Progress"),
    ("DELIVERED", "Delivered"),
    ("COMPLETED", "Completed"))

    orderNumber = models.AutoField(primary_key=True,auto_created=True)
    customer = models.ForeignKey(MedmeUser,related_name='orders', on_delete=models.CASCADE, blank=False)
    address = models.TextField(default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_CONFIRMED')
    productCharges = models.IntegerField(default=0)
    deliveryCharges = models.IntegerField(default=0)
    extraCharges = models.IntegerField(default=0)
    totalBill = models.IntegerField(default=0)
    paymentReceived = models.IntegerField(default=0)
    items = models.ManyToManyField(Medicine, related_name='items',blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
