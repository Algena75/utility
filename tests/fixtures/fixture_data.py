import pytest

test_data = {
    "street": "Onemore str.", 
    "house_number": 1, 
    "bld_number": 1, 
    "apartments": [
        {
            "number": 1, 
            "square": 36.000, 
            "counters": [
                {
                    "number": "00002"
                }
            ]
        }
    ]
}


@pytest.fixture
def building():
    from apartments.models import Apartment, Building, Counter
    building = Building.objects.create(
        street="Some str.", house_number=1
    )
    apartment = Apartment.objects.create(
        building=building, square=36.0, number=1
    )
    Counter.objects.create(apartment=apartment, number='00001')
    return building


@pytest.fixture
def new_building():
    return test_data
