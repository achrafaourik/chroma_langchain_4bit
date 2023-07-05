"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from items import views


router = DefaultRouter()
router.register('items', views.ItemViewSet)

app_name = 'items'

urlpatterns = [
    path('', include(router.urls)),
]
