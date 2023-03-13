from rest_framework import serializers

from network.models import Distributor


class ManufacturerValidator:
    def __init__(self, manufacturer_type: str = 'factory'):
        self.manufacturer_type: str = manufacturer_type

    def __call__(self, distributor: dict):
        distributor_type: str = distributor['distributor'].type
        if distributor_type != Distributor.Type[self.manufacturer_type]:
            raise serializers.ValidationError(
                f"Only distributor with the type '{self.manufacturer_type}' may be set as 'manufacturer'"
            )
