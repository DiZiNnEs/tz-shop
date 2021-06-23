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

    @action(detail=True, methods=['put', 'patch'])
    def cancel_order(self, request, pk=None):
        data = self.queryset.filter(id=pk)
        data.update(is_active=False)
        return Response(status.HTTP_200_OK)


class BuyProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = BuyProduct.objects.all()
    serializer_class = BuyProductSerializer
