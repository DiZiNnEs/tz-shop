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
    slug = models.SlugField(verbose_name='Slug товара')

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
        first_product = self.products.first()
        last_product = self.products.last()
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


class Report(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Продукт', related_name='product')
    revenue = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True,
                                  verbose_name='Выручка от продукт')
    profit = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True,
                                 verbose_name='Прибыль от продукт')
    number_of_units_sold = models.BigIntegerField(verbose_name='Количество проданных единиц товара/продукта',
                                                  help_text='проданные единицы товара')
    number_of_returns = models.BigIntegerField(verbose_name='Количество возвратов товара/продукта',
                                               help_text='количество возврата')

    def __str__(self) -> str:
        return f'Отчёт по {self.product.name}'

    class Meta:
        db_table = 'report'
        verbose_name = 'Отчеты'
        verbose_name_plural = 'Отчеты'
