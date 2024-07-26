from django.db import transaction
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from apartments.models import Building
from bills.serializers import BuildingBillSerializer
from bills.tasks import calculate_bills
from bills.validators import validate_period


class BillCalculationView(APIView):
    serializer_class = BuildingBillSerializer

    def get(self, request, *args, **kwargs):
        house = get_object_or_404(Building, pk=kwargs.get('house_nr'))
        month, year = validate_period(kwargs.get('month_nr'),
                                      kwargs.get('year_nr'))
        apartments = house.apartments.all()
        data = dict(address=str(house), period=f'{month}.{year}')
        bills = list()
        for apartment in apartments:
            bill = apartment.bills.filter(
                period__month=month, period__year=year
            ).first()
            if not bill:
                continue
            bills.append(
                model_to_dict(bill, fields=['water', 'community_property',
                                            'total', 'apartment'])
            )
        if not bills:
            raise ValidationError(f'Счета для дома {house} не найдены!')
        data.update(bills=bills)
        serializer = BuildingBillSerializer(data=data)
        return Response(serializer.initial_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        house = get_object_or_404(Building, pk=kwargs.get('house_nr'))
        month, year = validate_period(kwargs.get('month_nr'),
                                      kwargs.get('year_nr'))
        apartments = house.apartments.all()
        for apartment in apartments:
            try:
                with transaction.atomic():
                    job_params = dict(apartment_id=apartment.id,
                                      month=month,
                                      year=year)
                    transaction.on_commit(
                        lambda: calculate_bills.delay(job_params)
                    )
            except Exception as e:
                raise ValidationError(str(e))
            message = (f'Задача по расчёту счетов для дома {house} за '
                       f'{month}.{year} сформирована')
        return Response(message, status.HTTP_200_OK)
