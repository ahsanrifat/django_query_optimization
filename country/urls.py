from django.urls import path, include
from country.views import (
    test_api,
    revenue_range,
    get_country_city_all_report,
    get_a_countrys_areas,
    revenue_aggregate,
    country_wise_largest_city,
    country_wise_total_land,
    country_wise_city_list,
)

urlpatterns = [
    path("populate_db/", test_api),
    path("rev_range/", revenue_range),
    path("full_report/", get_country_city_all_report),
    path("country/areas", get_a_countrys_areas),
    path("revenue/report/", revenue_aggregate),
    path("largest/city/", country_wise_largest_city),
    path("total_land/", country_wise_total_land),
    path("city_list/", country_wise_city_list),
]
