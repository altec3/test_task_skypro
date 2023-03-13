from django.urls import path, include
from rest_framework import routers

from network.views import (
    ContactsViewSet, ProductViewSet, DistributorViewSet, LinkViewSet, NetworkViewSet
)

router = routers.SimpleRouter()
router.register('contacts', ContactsViewSet)
router.register('product', ProductViewSet)
router.register('distributor', DistributorViewSet)
router.register('distributor_link', LinkViewSet)
router.register('', NetworkViewSet)

app_name = 'network'
urlpatterns = [
    path('', include(router.urls)),
]
