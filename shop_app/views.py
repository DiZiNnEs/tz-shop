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
        count_of_product = request.data.get('products')
        for count in count_of_product:
            product = Product.objects.get(id=count)
            numbers_of_units_product = product.number_of_units
            if int(numbers_of_units_product) < int(number_of_units_order):
                return Response({f'Not enough product quantity {count_of_product[count]}'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                result = int(numbers_of_units_product) - int(number_of_units_order)
                Product.objects.filter(id=request.data.get(count)).update(number_of_units=result)
        return super().create(request, args, kwargs)

    @action(detail=True, methods=['put', 'patch'], url_path='cancel-order')
    def cancel_order(self, request, pk=None):
        if pk is None:
            return Response({'Order id not transferred'}, status.HTTP_400_BAD_REQUEST)
        try:
            data = self.queryset.filter(id=pk)
            data.update(is_active=False)
            return Response({'Order cancelled'}, status.HTTP_200_OK)
        except:
            return Response({'Order does not exist or not found'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'patch', 'put']
    queryset = BuyProduct.objects.all()
    serializer_class = BuyProductSerializer

    def create(self, request, *args, **kwargs):
        quantity = request.data.get('quantity')
        product_id = request.data.get('product')
        quantity_product_from_db = Product.objects.get(id=product_id).number_of_units
        if int(quantity_product_from_db) < int(quantity):
            return Response({'Not enough product quantity'}, status.HTTP_204_NO_CONTENT)
        else:
            result = int(quantity_product_from_db) - int(quantity)
            Product.objects.filter(id=product_id).update(number_of_units=result)
        return super().create(request, args, kwargs)

    @action(detail=True, methods=['put', 'patch'], url_path='cancel-order')
    def cancel_order(self, request, pk=None):
        if pk is None:
            return Response({'Order id not transferred'}, status.HTTP_400_BAD_REQUEST)
        try:
            data = self.queryset.filter(id=pk)
            data.update(is_active=False)
            return Response({'Order cancelled'}, status.HTTP_200_OK)
        except:
            return Response({'Order does not exist or not found'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
