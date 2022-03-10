from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from country import models as cm
from django.db.models import Q
import ipdb
from datetime import date
from django.db import connection


@api_view()
def test_api(request):
    country_list = cm.Country.objects.all()

    return Response({"message": country_list.values()})


@api_view()
def revenue_range(request):
    rev_list = cm.Revenue.objects.filter(
        # Q(country_name__startswith="USA"),
        Q(date__gt=date(2005, 5, 2))
        | Q(date__lt=date(2022, 5, 6))
    )
    """ 
    SELECT "revenue"."id", "revenue"."date", "revenue"."amount", "revenue"."country_id" 
    FROM "revenue" 
    WHERE ("revenue"."date" > '2005-05-02' OR "revenue"."date" < '2022-05-06'); args=('2005-05-02', '2022-05-06')"""

    # ipdb.set_trace()
    return Response({"message": rev_list.values()})


@api_view()
def get_country_city_all_report(request):
    """combined full report"""
    cursor = connection.cursor()
    query = """
    SELECT area.area_name,city.city_name,country.country_name FROM area 
    join city on area.city_id=city.id
    join country on country_id=country.id
    """
    query2 = """
    select city_id from area
    """
    # cursor.execute(query)
    # row = cursor.fetchall()
    row = cm.Area.objects.select_related("city")
    ipdb.set_trace()
    return Response({"data": row.values()})
