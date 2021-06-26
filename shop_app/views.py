from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from shop_app.models import (
    Product,
    ProductOrder,
    BuyProduct,
    Report,
)
from shop_app.serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    BuyProductSerializer,
    ReportSerializer
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
    report = Report.objects.all()
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    def create(self, request, *args, **kwargs):
        number_of_units_order = request.data.get('number_of_units')
        count_of_product = request.data.get('products')
        for count in count_of_product:
            product = Product.objects.get(id=count)
            numbers_of_units_product = product.number_of_units
            if int(numbers_of_units_product) < int(number_of_units_order):
                return Response({f'Not enough product quantity {product.name} product'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                result = int(numbers_of_units_product) - int(number_of_units_order)
                Product.objects.filter(id=request.data.get(count)).update(number_of_units=result)
                self.__update_report(product=product)
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

    def __update_report(self, product, *args, **kwargs):
        try:
            if self.report.get(product=product):
                report = self.report.filter(product=product)
                report.update(product=product, revenue=report.get().revenue + product.price,
                              profit=report.get().profit + product.cost_price,
                              number_of_units_sold=report.get().number_of_units_sold + 1,
                              number_of_returns=report.get().number_of_returns)
        except:  # DoesNotExist
            self.report.create(product=product, revenue=product.price,
                               profit=product.cost_price,
                               number_of_units_sold=1,
                               number_of_returns=0)


class BuyProductViewSet(viewsets.ModelViewSet):
    report = Report.objects.all()
    http_method_names = ['post', 'patch', 'put']
    queryset = BuyProduct.objects.all()
    serializer_class = BuyProductSerializer

    def create(self, request, *args, **kwargs):
        quantity = request.data.get('quantity')
        product_id = request.data.get('product')
        product = Product.objects.get(id=product_id)
        quantity_product_from_db = Product.objects.get(id=product_id).number_of_units
        if int(quantity_product_from_db) < int(quantity):
            return Response({'Not enough product quantity'}, status.HTTP_204_NO_CONTENT)
        else:
            self.__update_report(product=product, option=1)
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

    def __update_report(self, product,  option, *args, **kwargs,):
        if option is None:
            raise Exception('You must pass the option')
        if option == 1:
            try:
                if self.report.get(product=product):
                    report = self.report.filter(product=product)
                    report.update(product=product, revenue=report.get().revenue + product.price,
                                  profit=report.get().profit + product.cost_price,
                                  number_of_units_sold=report.get().number_of_units_sold + 1,
                                  number_of_returns=report.get().number_of_returns)
            except:  # DoesNotExist
                self.report.create(product=product, revenue=product.price,
                                   profit=product.cost_price,
                                   number_of_units_sold=1,
                                   number_of_returns=0)
        elif option == 2:
            ...


class ReportViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
