"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from coins import views


router = DefaultRouter()
router.register('coins', views.CoinViewSet)

app_name = 'coins'

urlpatterns = [
    path('', include(router.urls)),
]
