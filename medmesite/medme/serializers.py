from rest_framework import serializers

from django.contrib.auth.models import User

from medme.models import Order, Medicine, Customer, Composition, Drug, OrderItems


class DrugSerializer(serializers.HyperlinkedModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
    class Meta:
        model = Drug
        fields = ('id', 'name')


class CompositionSerializer(serializers.HyperlinkedModelSerializer):
    drug_name = serializers.ReadOnlyField(source='drug.name')
    drug_id = serializers.ReadOnlyField(source='drug.id')

    class Meta:
        model = Composition
        fields = ('drug_id', 'drug_name', 'potency')


class MedicineSerializer(serializers.HyperlinkedModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    form_name = serializers.ReadOnlyField(source='form.form')
    compositions = CompositionSerializer(many=True, read_only=True)

    class Meta:
        model = Medicine
        fields = ('name', 'company_name', 'form_name', 'compositions', 'price', 'created')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
    class Meta:
        model = Customer
        fields = ('id', 'phone', 'email', 'name', 'address')


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    # order_number = serializers.ReadOnlyField(source='order.orderNumber')
    # medicine_id = serializers.ReadOnlyField(source='medicine.id')
    # medicine_name = serializers.ReadOnlyField(source='medicine.name')
    medicine = MedicineSerializer(read_only=True)

    class Meta:
        model = OrderItems
        fields = ('medicine', 'quantity')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    customer_id = serializers.ReadOnlyField(source='customer.id')
    items = OrderItemSerializer(source='orderitems_set', many=True, read_only=True)
    customer = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('orderNumber', 'customer_name', 'customer_id', 'status', 'totalBill', 'created', 'customer', 'items')


class OrderByUserSerializer(serializers.HyperlinkedModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'orders')
