from django.contrib import admin

from apartments.models import (Apartment, Building, Counter, CounterValue,
                               Period)
from bills.models import Bill, Tariff


class CounterInline(admin.TabularInline):
    model = Counter


class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'street',
        'house_number',
        'bld_number',
    )
    list_filter = ('street',)


class ApartmentAdmin(admin.ModelAdmin):
    inlines = [CounterInline,]
    list_display = (
        'pk',
        'building',
        'number',
        'square',
    )
    list_filter = ('building',)


class CounterAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'apartment',
        'number'
    )


class PeriodAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'month',
        'year'
    )


class CounterValueAdmin(admin.ModelAdmin):
    list_display = ('counter', 'period', 'value')


class TariffAdmin(admin.ModelAdmin):
    pass


class BillAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'period', 'water', 'community_property',
                    'total')


admin.site.register(Building, BuildingAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Counter, CounterAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(CounterValue, CounterValueAdmin)
