import pytest

@pytest.fixture
def period():
    from apartments.models import Period
    return Period.objects.create(month=7, year=2024)
