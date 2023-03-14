from rest_framework import serializers

from network.models import Network, Link, Distributor, Product, Contacts
from network.validators import ManufacturerValidator


class ContactsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Contacts"""

    class Meta:
        model = Contacts
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор модели Product"""

    class Meta:
        model = Product
        fields = '__all__'


class DistributorSerializer(serializers.ModelSerializer):
    """Сериализатор модели Distributor"""

    class Meta:
        model = Distributor
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор модели Link"""

    id = serializers.IntegerField()

    distributor = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Distributor.objects.all()
    )
    supplier = serializers.SlugRelatedField(
        required=False,
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
        read_only_fields = ('debt', 'created',)


class NetworkSerializer(serializers.ModelSerializer):
    """Сериализатор модели Network"""

    manufacturer = LinkSerializer(validators=[ManufacturerValidator()])
    distributor_1 = LinkSerializer()
    distributor_2 = LinkSerializer()

    class Meta:
        model = Network
        fields = '__all__'

    def create(self, validated_data: dict) -> Network:
        #: Данные звеньев, которые необходимо добавить в сеть
        manufacturer_data = validated_data.pop('manufacturer')
        distributor_1_data = validated_data.pop('distributor_1')
        distributor_2_data = validated_data.pop('distributor_2')

        #: Получение звеньев для включения в сеть
        manufacturer = Link.objects.get(
            id=manufacturer_data.pop('id'),
            distributor=manufacturer_data.pop('distributor'),
        )
        distributor_1 = Link.objects.get(id=distributor_1_data.pop('id'),)
        distributor_2 = Link.objects.get(id=distributor_2_data.pop('id'),)

        #: Создание сети
        instance = Network.objects.create(
            manufacturer=manufacturer,
            distributor_1=distributor_1,
            distributor_2=distributor_2,
            **validated_data
        )
        return instance

    def update(self, instance: Network, validated_data: dict) -> Network:
        #: Данные для обновления полей
        manufacturer_data = validated_data.pop('manufacturer')
        distributor_1_data = validated_data.pop('distributor_1')
        distributor_2_data = validated_data.pop('distributor_2')

        #: Обновление значений полей
        instance.manufacturer = Link.objects.get(
            id=manufacturer_data.pop('id', instance.manufacturer.id),
            distributor=manufacturer_data.pop('distributor', instance.manufacturer.distributor)
        )
        instance.distributor_1 = Link.objects.get(id=distributor_1_data.pop('id', instance.distributor_1.id),)
        instance.distributor_2 = Link.objects.get(id=distributor_2_data.pop('id', instance.distributor_2.id),)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        return instance
