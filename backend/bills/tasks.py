from celery import shared_task

from bills.services import calculate_bill


@shared_task()
def calculate_bills(job_params: dict):
    """
    Задача вызывает функцию расчёта квартплаты для заданной квартиры
    в заданный период времени.
    """
    calculate_bill(job_params.get('apartment_id'),
                   job_params.get('month'),
                   job_params.get('year'))
