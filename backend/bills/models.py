from datetime import datetime

from django.db import models

from apartments.models import Apartment, Period


class Tariff(models.Model):
    WATER = 'WA'
    COMMUNITY_PROPERTY = 'CP'
    TARIFF_CHOICES = {
        WATER: 'Вода',
        COMMUNITY_PROPERTY: 'Содержание общего имущества'
    }
    name = models.CharField(
        max_length=2,
        choices=TARIFF_CHOICES,
        default=WATER,
        verbose_name='Вид платежа'
    )
    value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=1.0,
        verbose_name='Тариф'
    )
    from_date = models.DateField(
        null=False,
        default=datetime.today,
        verbose_name='Дата ввода тарифа'
    )
    until_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата отмены тарифа'
    )
    is_current = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Статус тарифа'
    )

    def __str__(self) -> str:
        until_date = self.until_date if self.until_date else None
        return f'{self.name} {self.from_date} - {until_date}'


class Bill(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='bills',
        null=False
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        null=False,
        related_name='bills'
    )
    water = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Вода'
    )
    community_property = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Содержание общего имущества'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='ИТОГО'
    )
