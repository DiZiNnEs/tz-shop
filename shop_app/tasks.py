# Create your tasks here

from celery import shared_task
from shop_app.models import Report


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_report():
    return Report.objects.count()


@shared_task
def rename_report(widget_id, name):
    w = Report.objects.get(id=widget_id)
    w.name = name
    w.save()
