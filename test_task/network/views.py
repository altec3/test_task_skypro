from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions

from network.models import Contacts, Product, Distributor, Link, Network
from network.serializers import (ContactsSerializer,
                                 ProductSerializer, DistributorSerializer,
                                 LinkSerializer, NetworkSerializer
                                 )


@extend_schema_view(
    list=extend_schema(summary="Все контакты"),
    create=extend_schema(summary="Создать контакты"),
    retrieve=extend_schema(summary="Подробная контактная информация"),
    partial_update=extend_schema(summary="Изменить контакты"),
    destroy=extend_schema(summary="Удалить контакты"),
)
class ContactsViewSet(viewsets.ModelViewSet):

    queryset = Contacts.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContactsSerializer


@extend_schema_view(
    list=extend_schema(summary="Вся продукция"),
    create=extend_schema(summary="Создать продукт"),
    retrieve=extend_schema(summary="Подробно о продукте"),
    partial_update=extend_schema(summary="Изменить продукт"),
    destroy=extend_schema(summary="Удалить продукт"),
)
class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer


@extend_schema_view(
    list=extend_schema(summary="Все дистрибьюторы"),
    create=extend_schema(summary="Создать дистрибьютора"),
    retrieve=extend_schema(summary="Подробно о дистрибьюторе"),
    partial_update=extend_schema(summary="Изменить данные о дистрибьюторе"),
    destroy=extend_schema(summary="Удалить дистрибьютора"),
)
class DistributorViewSet(viewsets.ModelViewSet):

    queryset = Distributor.objects.all().select_related('contacts')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DistributorSerializer


@extend_schema_view(
    list=extend_schema(summary="Список всех звеньев сети"),
    create=extend_schema(summary="Создать звено сети"),
    retrieve=extend_schema(summary="Подробно о звене сети"),
    partial_update=extend_schema(summary="Изменить звено сети"),
    destroy=extend_schema(summary="Удалить звено сети"),
)
class LinkViewSet(viewsets.ModelViewSet):

    queryset = Link.objects.all().prefetch_related('products').select_related('distributor', 'supplier')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer
    #: Фильтрация цепочки "Распространитель-Поставщик" по стране
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']


@extend_schema_view(
    list=extend_schema(summary="Список всех торговых сетей"),
    create=extend_schema(summary="Создать торговую сеть"),
    retrieve=extend_schema(summary="Подробно о торговой сети"),
    partial_update=extend_schema(summary="Изменить торговую сеть"),
    destroy=extend_schema(summary="Удалить торговую сеть"),
)
class NetworkViewSet(viewsets.ModelViewSet):

    queryset = Network.objects.all().select_related('manufacturer', 'distributor_1', 'distributor_2')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NetworkSerializer
