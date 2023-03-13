from rest_framework import serializers

from network.models import Network, Link, Distributor, Product, Contacts
from network.validators import ManufacturerValidator


class ContactsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Contacts"""

    class Meta:
        model = Contacts
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели Product"""

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)


class DistributorSerializer(serializers.ModelSerializer):
    """Сериализатор модели Distributor"""

    class Meta:
        model = Distributor
        fields = '__all__'
        read_only_fields = ('id',)


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор модели Link"""

    distributor = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Distributor.objects.all()
    )
    supplier = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Distributor.objects.all()
    )
    products = serializers.SlugRelatedField(
        slug_field='model',
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ('id', 'debt', 'created',)


class NetworkSerializer(serializers.ModelSerializer):
    """Сериализатор модели Network"""

    class Meta:
        model = Network
        fields = '__all__'
        read_only_fields = ('id',)
