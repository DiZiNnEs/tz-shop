from rest_framework.routers import DefaultRouter

from shop_app.views import (
    ProductViewSet,
    ProductOrderViewSet,
    BuyProductViewSet,
)

router = DefaultRouter()

router.register(r'products', ProductViewSet)
router.register(r'product-orders', ProductOrderViewSet)
router.register(f'buy-product', BuyProductViewSet)
