from datetime import date

from django.shortcuts import get_object_or_404

from apartments.models import Apartment, Period, CounterValue
from backend.constants import constants
from bills.models import Bill, Tariff


def calculate_bill(apartment_id, month, year):
    period, _ = Period.objects.get_or_create(month=month, year=year)
    apartment = get_object_or_404(Apartment, pk=apartment_id)
    water_tariff = Tariff.objects.filter(
        name='WA', from_date__lte=date(year, month, 1)
    ).order_by('from_date').last().value
    cp_tariff = Tariff.objects.filter(
        name='CP', from_date__lte=date(year, month, 1)
    ).order_by('from_date').last().value
    counters = apartment.counters.all()
    water_difference = 0
    for counter in counters:
        counter_values = CounterValue.objects.filter(
            counter=counter, period__year__lte=year, period__month__lte=month
        ).order_by('-period__year', '-period__month')
        if counter_values.count() >= 2:
            if all(counter_values[0].period.year == year,
                   counter_values[0].period.month == month):

                water_difference += (counter_values[0].value -
                                     counter_values[1].value)
            else:
                water_difference += constants.NORMA
                CounterValue.objects.create(
                    counter=counter, period=period,
                    value=(counter_values[0].value + constants.NORMA)
                )
        elif counter_values.count() == 1:
            if all(counter_values[0].period.year == year,
                   counter_values[0].period.month == month):

                water_difference += counter_values[0].value
            else:
                water_difference += constants.NORMA
                CounterValue.objects.create(
                    counter=counter, period=period,
                    value=(counter_values[0].value + constants.NORMA)
                )
        else:
            water_difference += constants.NORMA
            CounterValue.objects.create(
                counter=counter, period=period, value=constants.NORMA
            )

    Bill.objects.create(
        apartment=apartment,
        period=period,
        water=water_difference * water_tariff,
        community_property=apartment.square * cp_tariff,
        total=water_difference * water_tariff + apartment.square * cp_tariff
    )
