# Generated by Django 3.2.4 on 2021-06-25 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0004_buyproduct_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(verbose_name='Slug товара'),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True, verbose_name='Выручка от продукт')),
                ('profit', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True, verbose_name='Прибыль от продукт')),
                ('number_of_units_sold', models.BigIntegerField(help_text='проданные единицы товара', verbose_name='Количество проданных единиц товара/продукта')),
                ('number_of_returns', models.BigIntegerField(help_text='количество возврата', verbose_name='Количество возвратов товара/продукта')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='shop_app.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Отчеты',
                'verbose_name_plural': 'Отчеты',
                'db_table': 'report',
            },
        ),
    ]
