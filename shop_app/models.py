from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название товара')
    is_active = models.BooleanField(default=True, verbose_name='Активность товара')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление товара')
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения товара')
    cost_price = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='Себестоимость товара',
                                     help_text='себестоимость товара')
    price = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='Цена товара:')
    number_of_units = models.BigIntegerField(verbose_name='Количество товара')
    slug = models.SlugField(verbose_name='Slug товара:')

    def __str__(self) -> str:
        return f'Товар {self.name}'

    def get_name(self) -> str:
        return self.name

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductOrder(models.Model):
    products = models.ManyToManyField(Product, verbose_name='Продукт')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик')
    number_of_units = models.BigIntegerField(verbose_name='Количество заказанных товара')
    is_active = models.BooleanField(default=True, verbose_name='Активность заказа')
    delivery_address = models.CharField(max_length=256, verbose_name='Адресс доставки')

    def __str__(self) -> str:
        first = self.products.first()
        last = self.products.last()
        first_product = getattr(first, 'first', 'продукт')
        last_product = getattr(last, 'last', 'продукт')
        return f'Заказ на {first_product}, {last_product} и другие ... от {self.customer.username}'

    class Meta:
        db_table = 'product_order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class BuyProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель товара')
    quantity = models.BigIntegerField(verbose_name='Количество единиц товара')
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Покупка товара {self.product.name} от {self.buyer.username}'

    class Meta:
        db_table = 'buy_product'
        verbose_name = 'Покупа товара'
        verbose_name_plural = 'Покупка товаров'
