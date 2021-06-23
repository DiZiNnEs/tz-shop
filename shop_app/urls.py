from django.urls import path, include

from shop_app.router import router

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
