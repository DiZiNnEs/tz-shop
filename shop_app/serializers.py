from django.contrib.auth.models import User
from rest_framework import serializers

from shop_app.models import (
    Product,
    ProductOrder,
    BuyProduct
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'is_active', 'date_added', 'date_modified', 'cost_price', 'price', 'number_of_units', 'slug',)


class ProductOrderSerializer(serializers.ModelSerializer):
    products_id = serializers.PrimaryKeyRelatedField(source='products', many=True, queryset=Product.objects.all(),
                                                     required=False)
    products = ProductSerializer(many=True, read_only=True)
    customer_name = serializers.StringRelatedField(source='customer')

    def to_internal_value(self, data):
        data_copy = data.copy()
        if self.context['request'].user.id is None:
            # pass
            raise Exception('Context object is not have user id')
        user = User.objects.get(id=self.context['request'].user.id)
        # user = User.objects.get(id=1)
        if user is None:
            raise Exception('User object is None')
        data_copy['customer'] = user.id
        return super().to_internal_value(data_copy)

    class Meta:
        model = ProductOrder
        fields = (
            'products_id', 'products', 'customer_name', 'customer', 'number_of_units', 'is_active',
            'delivery_address',)
        extra_kwargs = {
            'products': {'read_only': True, 'write_only': False},
            'products_id': {'required': False}
        }


class BuyProductSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        data_copy = data.copy()
        if self.context['request'].user.id is None:
            raise Exception('Context object does not have  have user id')
        user = User.objects.get(id=self.context['request'].user.id)
        if user is None:
            raise Exception('User object is None')
        data_copy['buyer'] = user.id

        return super().to_internal_value(data_copy)

    class Meta:
        model = BuyProduct
        fields = ('product', 'buyer', 'is_active', 'quantity')
