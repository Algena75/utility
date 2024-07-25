from decimal import Decimal
from rest_framework import serializers

from apartments.models import Apartment, Building, Counter, Period


class CounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counter
        fields = ('number',)


class ApartmentSerializer(serializers.ModelSerializer):
    counters = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Apartment
        fields = ('number', 'square', 'counters')


class ApartmentWriteSerializer(serializers.ModelSerializer):
    counters = CounterSerializer(many=True)
    # square = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        model = Apartment
        fields = ('number', 'square', 'counters')


class HouseSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    apartments = ApartmentSerializer(read_only=True, many=True)

    class Meta:
        model = Building
        fields = ('id', 'address', 'apartments')

    def get_address(self, obj):
        address = f'{obj.street}, д.{obj.house_number}'
        if obj.bld_number:
            address += f', корп.{obj.bld_number}'
        return address


class HouseWriteSerializer(serializers.ModelSerializer):
    apartments = ApartmentWriteSerializer(many=True)

    class Meta:
        model = Building
        fields = ('street', 'house_number', 'bld_number', 'apartments')

    def create(self, validated_data):
        print('initial data: ', self.initial_data)
        print('validated data: ', validated_data)
        if 'apartments' not in self.initial_data:
            house = Building.objects.create(**validated_data)
            return house
        apartments = validated_data.pop('apartments')
        house, _ = Building.objects.get_or_create(**validated_data)
        for apartment in apartments:
            counters = apartment.pop('counters')
            current_apartment = Apartment.objects.filter(
                building=house,
                number=apartment.get('number')
            ).first()
            if not current_apartment:
                current_apartment = Apartment.objects.create(
                    building=house,
                    number=apartment.get('number'),
                    square = Decimal(apartment.get('square'))
                )
            if counters:
                for counter in counters:
                    Counter.objects.create(number=counter.popitem(True)[1],
                                           apartment=current_apartment)
        return house
