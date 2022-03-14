from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from country import models as cm
from django.db.models import Q, F, Sum, Subquery, OuterRef
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
    # row = cm.Area.objects.select_related("city")
    row = cm.Country.objects.prefetch_related("cities")
    return Response({"data": row.values()})


@api_view()
def get_a_countrys_areas(request):
    """combined full report"""
    c = cm.Country.objects.filter(id=1)
    c2 = cm.City.objects.filter(country__in=c.values("id"))
    # row = cm.Area.objects.filter(city__in=c2.values("id"))
    # row = cm.Area.objects.filter(city__in=c2.values("id")).annotate(
    # 2 F's means two full join
    #     City_name=F("city__city_name"), Country_name=F("city__country__country_name")
    # )
    row = cm.Area.objects.filter(city__in=c2.values("id")).annotate(
        City_name=F("city__city_name")
    )
    return Response({"data": row.values()})


@api_view()
def get_a_countrys_areas(request):
    """combined full report"""
    c = cm.Country.objects.filter(id=1)
    c2 = cm.City.objects.filter(country__in=c.values("id"))
    # row = cm.Area.objects.filter(city__in=c2.values("id"))
    # row = cm.Area.objects.filter(city__in=c2.values("id")).annotate(
    #     City_name=F("city__city_name"), Country_name=F("city__country__country_name")
    # )
    row = cm.Area.objects.filter(city__in=c2.values("id")).annotate(
        City_name=F("city__city_name")
    )
    return Response({"data": row.values()})


@api_view()
def revenue_aggregate(request):
    row = (
        cm.Revenue.objects.values("country")
        .order_by("country")
        .annotate(total_revenue=Sum("amount"), country_=F("country__country_name"))
    )
    return Response({"data": row})


@api_view()
def country_wise_largest_city(request):
    city_qr = cm.City.objects.filter(country=OuterRef("pk")).order_by("-land")
    result = (
        cm.Country.objects.filter(country_name__startswith="g")
        .values("country_name")
        .annotate(largest_city=Subquery(city_qr.values("city_name")[:1]))
    )[:5]
    return Response({"data": result.values("country_name", "largest_city")})


import random, string


def give_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def bulk_insert():
    economy_type = ["Business", "Industry", "Agriculture", "Tourism"]
    instence_list = []
    for _ in range(100000):
        instence_list.append(
            cm.Country(
                country_name=give_random_string(8),
                land=random.randint(10000000, 1000000000),
                population=random.randint(10000000, 1000000000),
                average_age=random.randint(10, 100),
                economy_type=random.choice(economy_type),
            )
        )
    cm.Country.objects.bulk_create(instence_list)
    print("Bulk Insert Done")


def bulk_insert_city():

    instence_list = []
    for _ in range(99000):
        country_id = random.randint(1, 100000)
        print("Country id-->", country_id)
        instence_list.append(
            cm.City(
                city_name=give_random_string(8),
                land=random.randint(10000000, 1000000000),
                mayor=give_random_string(6),
                country=cm.Country.objects.get(id=country_id),
            )
        )
    cm.City.objects.bulk_create(instence_list)
    print("Bulk Insert Done")
