from rest_framework import serializers

from network.models import Network, Link, Distributor, Product, Contacts


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
