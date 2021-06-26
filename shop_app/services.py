from django.db.models import QuerySet

from shop_app.models import Product


def update_report(product: Product, report: QuerySet, option: int, *args, **kwargs) -> None:
    if option is None:
        raise Exception('You must pass the option')
    if option == 1:
        try:
            if report.get(product=product):
                report = report.filter(product=product)
                report.update(product=product, revenue=report.get().revenue + product.price,
                              profit=report.get().profit + product.cost_price,
                              number_of_units_sold=report.get().number_of_units_sold + 1,
                              number_of_returns=report.get().number_of_returns)
        except:  # DoesNotExist
            report.create(product=product, revenue=product.price,
                          profit=product.cost_price,
                          number_of_units_sold=1,
                          number_of_returns=0)
    elif option == 2:
        if report.get(product=product):
            report = report.filter(product=product)
            report.update(product=product, revenue=report.get().revenue + product.price,
                          profit=report.get().profit + product.cost_price,
                          number_of_units_sold=report.get().number_of_units_sold + 1,
                          number_of_returns=report.get().number_of_returns - 1)
