from django.urls import include, path
from rest_framework import routers

from apartments.views import HouseViewSet
from bills.views import BillCalculationView

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('houses', HouseViewSet, basename='house')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('bills/<int:house_nr>/<int:month_nr>/<int:year_nr>/',
         BillCalculationView.as_view(), name='bill')
]
