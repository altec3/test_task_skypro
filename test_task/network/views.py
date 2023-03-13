from rest_framework import viewsets, permissions

from network.models import Contacts, Product, Distributor, Link, Network
from network.serializers import (ContactsSerializer,
                                 ProductSerializer, DistributorSerializer,
                                 LinkSerializer, NetworkSerializer
                                 )


class ContactsViewSet(viewsets.ModelViewSet):
    """Представление для обработки запроса на эндпоинт /network/contacts/

    Действия над объектом Contacts
    """
    queryset = Contacts.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContactsSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Представление для обработки запроса на эндпоинт /network/product/

    Действия над объектом Product
    """
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer


class DistributorViewSet(viewsets.ModelViewSet):
    """Представление для обработки запроса на эндпоинт /network/distributor/

    Действия над объектом Distributor
    """
    queryset = Distributor.objects.all().select_related('contacts')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DistributorSerializer


class LinkViewSet(viewsets.ModelViewSet):
    """Представление для обработки запроса на эндпоинт /network/link/

    Действия над объектом Link
    """
    queryset = Link.objects.all().prefetch_related('products').select_related('distributor', 'supplier')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """Представление для обработки запроса на эндпоинт /network/

    Действия над объектом Network
    """
    queryset = Network.objects.all().select_related('manufacturer', 'distributor_1', 'distributor_2')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkSerializer
