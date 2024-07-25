from rest_framework import status, viewsets

from apartments.models import Apartment, Building, Counter, Period
from apartments.serializers import HouseSerializer, ApartmentSerializer, HouseWriteSerializer

class HouseViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    http_method_names = ('get', 'post')

    def get_serializer_class(self):
            if self.request.method == 'GET':
                return HouseSerializer
            else:
                return HouseWriteSerializer
