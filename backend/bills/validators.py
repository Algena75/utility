from datetime import datetime

from rest_framework.serializers import ValidationError


def validate_period(month, year):
    if month not in range(1, 13):
        raise ValidationError('Месяц должен быть в диапазоне от 1 до 12')
    if year < 2023 or year > datetime.now().year:
        raise ValidationError(
            f'Год должен быть в диапазоне от 2023 до {datetime.now().year}'
        )
    return month, year
