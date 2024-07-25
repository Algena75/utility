from rest_framework import status, viewsets
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from apartments.models import Building
from bills.models import Bill, Tariff
from bills.serializers import BuildingBillSerializer, BillSerializer
from bills.services import calculate_bill
from bills.validators import validate_period

class BillCalculationView(APIView):
    serializer_class = BuildingBillSerializer

    def get(self, request, *args, **kwargs):
        house = get_object_or_404(Building, pk=kwargs.get('house_nr'))
        month, year = validate_period(kwargs.get('month_nr'), kwargs.get('year_nr'))
        apartments = house.apartments.all()
        print('apartments>>>', apartments)
        data = dict(address=str(house), period=f'{month}.{year}')
        bills = list()
        for apartment in apartments:
            bill = apartment.bills.filter(period__month=month, period__year=year).first()
            if not bill:
                raise ValidationError(f'Счета для квартиры {apartment} не найдены!')
            print('bill>>>', bill)
            print('bill>>>', model_to_dict(bill, fields=['water', 'community_property', 'total', 'apartment']))
            bills.append(model_to_dict(bill, fields=['water', 'community_property', 'total', 'apartment']))
        data.update(bills=bills)
        serializer = BuildingBillSerializer(data=data)
        return Response(serializer.initial_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        house = get_object_or_404(Building, pk=kwargs.get('house_nr'))
        month, year = validate_period(kwargs.get('month_nr'), kwargs.get('year_nr'))
        apartments = house.apartments.all()
        for apartment in apartments:
            calculate_bill(apartment.id, month, year)
        return Response(f'Счета по дому {house} за {month}.{year} сформированы', status.HTTP_200_OK)
