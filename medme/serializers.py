from rest_framework import serializers

from django.contrib.auth.models import User

from medme.models import Order, Medicine, MedmeUser


class MedicineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Medicine
        fields = ('id', 'name', 'generic_name', 'company', 'doz', 'price')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())

    class Meta:
        model = MedmeUser
        fields = ('id', 'phone', 'email', 'name', 'address')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    customer_id = serializers.ReadOnlyField(source='customer.id')
    items = MedicineSerializer(many=True, read_only=True)
    customer = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('orderNumber', 'customer_name', 'customer_id', 'status', 'totalBill', 'created', 'customer', 'items')


class OrderByUserSerializer(serializers.HyperlinkedModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = MedmeUser
        fields = ('id', 'name', 'address', 'orders')
