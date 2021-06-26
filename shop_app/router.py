from rest_framework.routers import DefaultRouter

from shop_app.views import (
    ProductViewSet,
    ProductOrderViewSet,
    BuyProductViewSet,
    ReportViewSet,
)

router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'product-orders', ProductOrderViewSet)
router.register(r'buy-product', BuyProductViewSet)
router.register(r'report', ReportViewSet)
