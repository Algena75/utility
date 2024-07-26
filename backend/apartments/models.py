from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Building(models.Model):
    street = models.CharField(
        max_length=150,
        unique=False,
        null=False,
        verbose_name='Улица'
    )
    house_number = models.IntegerField(
        unique=False,
        null=False,
        verbose_name='Номер дома',
    )
    bld_number = models.PositiveIntegerField(
        # unique=False,
        null=True,
        blank=True,
        verbose_name='Номер корпуса',
    )

    def __str__(self) -> str:
        address = f'{self.street}, д.{self.house_number}'
        if self.bld_number:
            address += f', корп.{self.bld_number}'
        return address

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('street', 'house_number', 'bld_number'),
                name='unique_address'
            ),
            models.CheckConstraint(
                check=models.Q(house_number__gt=0),
                name='house_number_gt_0'
            ),
            models.CheckConstraint(
                check=models.Q(bld_number__range=(1, 20)),
                name='bld_number_gte_1_lte_20'
            ),
        ]


class Apartment(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='apartments',
        verbose_name='Дом'
    )
    number = models.PositiveIntegerField(verbose_name='Номер квартиры')
    square = models.DecimalField(
        decimal_places=3,
        max_digits=7,
        verbose_name='Площадь квартиры',
        null=False
    )

    def __str__(self) -> str:
        return f'{self.building}, кв.{self.number}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(square__gt=0),
                name='square_gt_0'
            ),
            models.UniqueConstraint(
                fields=('building', 'number'),
                name='unique_apartment_for_building'
            )
        ]


class Counter(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.DO_NOTHING,
        related_name='counters',
        verbose_name='Квартира',
        blank=False
    )
    number = models.CharField(
        max_length=128,
        verbose_name='№ счётчика',
        null=False,
        unique=True
    )

    def __str__(self) -> str:
        return self.number


class Period(models.Model):
    month = models.IntegerField(null=False, verbose_name='Месяц')
    year = models.IntegerField(
        null=False, verbose_name='Год',
        validators=[
            MinValueValidator(2023), MaxValueValidator(datetime.now().year)
        ]
    )

    def __str__(self) -> str:
        return f'{self.month}-{self.year}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('month', 'year'),
                name='unique_month_year'
            ),
            models.CheckConstraint(
                check=models.Q(month__range=(1, 12)),
                name='month_gte_1_gle_12'
            ),
        ]


class CounterValue(models.Model):
    counter = models.ForeignKey(
        Counter,
        on_delete=models.DO_NOTHING,
        related_name='values',
        verbose_name='№ счётчика'
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.DO_NOTHING,
        related_name='counters',
        verbose_name='Период'
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='Показания'
    )