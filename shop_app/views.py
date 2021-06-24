from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shop_app.models import (
    Product,
    ProductOrder,
    BuyProduct,
)
from shop_app.serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    BuyProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class ProductOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    def create(self, request, *args, **kwargs):
        number_of_units_order = request.data.get('number_of_units')
        product = Product.objects.get(id=request.data.get('products_id'))
        numbers_of_units_product = product.number_of_units
        if int(numbers_of_units_product) <= int(number_of_units_order):
            return Response({'Not enough products'}, status=status.HTTP_204_NO_CONTENT)
        else:
            result = int(numbers_of_units_product) - int(number_of_units_order)
            Product.objects.filter(id=request.data.get('products_id')).update(number_of_units=result)
        return super().create(request, args, kwargs)

    @action(detail=True, methods=['put', 'patch'])
    def cancel_order(self, request, pk=None):
        data = self.queryset.filter(id=pk)
        data.update(is_active=False)
        return Response(status.HTTP_200_OK)


class BuyProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = BuyProduct.objects.all()
    serializer_class = BuyProductSerializer
