from django.contrib import admin

from shop_app.models import (
    Product,
    ProductOrder,
    BuyProduct,
    Report
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(BuyProduct)
class BuyProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
