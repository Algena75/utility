from rest_framework import viewsets

from apartments.models import Building
from apartments.serializers import HouseSerializer, HouseWriteSerializer


class HouseViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    http_method_names = ('get', 'post')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return HouseSerializer
        else:
            return HouseWriteSerializer
