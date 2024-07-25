from rest_framework import serializers

from apartments.serializers import HouseSerializer
from bills.models import Bill


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('water', 'community_property', 'total')


class BuildingBillSerializer(HouseSerializer):
    # period = serializers.SerializerMethodField()
    # bills = BillSerializer(read_only=True, many=True)

    # class Meta:
    #     fields = ('period', 'bills')

    def get_period(self, obj):
        data = self.request.data
        return f'{data.get("month")}.{data.get("year")}'
