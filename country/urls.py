from django.urls import path, include
from country.views import test_api, revenue_range, get_country_city_all_report

urlpatterns = [
    path("test/", test_api),
    path("rev_range/", revenue_range),
    path("full_report/", get_country_city_all_report),
]
