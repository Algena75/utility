from http import HTTPStatus

import pytest
from django.shortcuts import get_object_or_404

from apartments.models import Building


@pytest.mark.django_db(transaction=True)
class TestBuildingAPI:

    def test_list_building(self, client, building):
        """
        Список домов доступен по адресу `/api/houses/`
        """
        response = client.get('/api/houses/')

        assert response.status_code == HTTPStatus.OK, (
            'Страница `/api/houses/` не найдена, проверьте этот адрес в '
            '*urls.py*.'
        )
        assert building.street in str(response.data)

    def test_new_building(self, client, new_building):
        """
        POST-запрос с корректными данными на `/api/houses/` создаёт новую
        запись в БД.
        """
        qty_before = Building.objects.all().count()
        response = client.post('/api/houses/', data=new_building)
        assert response.status_code == HTTPStatus.CREATED, (
            'Запись не создана, проверьте вьюсет.'
        )
        qty_after = Building.objects.all().count()
        assert qty_after == qty_before + 1

    def test_list_bills(self, client, building, period):
        """
        Список счетов доступен по адресу
        `/api/bills/{house_id}/{month}/{year}`
        """
        response = client.get(
            f'/api/bills/{building.pk}/{period.month}/{period.year}/'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Страница `/api/bills/` не найдена, проверьте этот адрес в '
            '*urls.py*.'
        )
        assert f'Счета для дома {building} не найдены!' in str(response.data)

    def test_new_bill(self, client, building, period):
        """
        POST-запрос по адресу `/api/bills/{house_id}/{month}/{year}` создаёт счёт.
        """
        response = client.post(
            f'/api/bills/{building.pk}/{period.month}/{period.year}/', data={}
        )
        assert response.status_code == HTTPStatus.OK, (
            'Счёт не создан, проверьте вью-функцию.'
        )
        message = (f'Задача по расчёту счетов для дома {building} за '
                   f'{period.month}.{period.year} сформирована')
        assert message in str(response.data)
