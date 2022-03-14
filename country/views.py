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
    """ 
    SELECT "country"."country_name",
        (SELECT U0."city_name" FROM "city" U0 WHERE U0."country_id" = ("country"."id") 
        ORDER BY U0."land" DESC LIMIT 1) AS "largest_city" 
    FROM "country" 
    WHERE "country"."country_name" LIKE 'g%' ESCAPE '\' LIMIT 5;
    """
    return Response({"data": result})


@api_view()
def country_wise_total_land(request):
    result = (
        cm.City.objects.values("country__country_name")
        .annotate(country_population=Sum("land"))
        .filter(country_population__gt=300000)
        .order_by("country_population")[:30]
    )
    """ 
    SELECT "country"."country_name", 
    SUM("city"."land") AS "country_land" FROM "city"
    INNER JOIN "country" ON ("city"."country_id" = "country"."id") 
    GROUP BY "country"."country_name" 
    ORDER BY "country_land" 
    ASC LIMIT 30; 
    """
    return Response({"data": result})


@api_view()
def country_wise_city_list(request):
    countries = list(cm.Country.objects.prefetch_related("cities"))
    data = []
    for country in countries:
        print("Country-->", country)
        country_dict = country.__dict__
        city_list = []
        for o in country_dict["_prefetched_objects_cache"]["cities"]:
            o = o.__dict__
            del o["_state"]
            city_list.append(o)
        # country_dict["_prefetched_objects_cache"]["cities"] = [
        #     o.__dict__ for o in country_dict["_prefetched_objects_cache"]["cities"]
        # ]
        country_dict["_prefetched_objects_cache"]["cities"] = city_list
        country_dict["cities"] = city_list
        del country_dict["_prefetched_objects_cache"]["cities"]
        del country_dict["_state"]
        print(country_dict)
        data.append(country_dict)
    return Response({"data": data})


# ----------------Helper Method------------------------

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


def bulk_insert_area():
    area_type = ["Metropolitan", "Downtown", "Urban", "Rural"]
    instence_list = []
    cities = list(cm.City.objects.all())
    for i in range(990000):
        city_id = random.randint(1, 99005)
        print("Number-->", i)
        instence_list.append(
            cm.Area(
                area_name=give_random_string(8),
                maintain_cost=random.randint(10000, 1000000),
                chairman=give_random_string(6),
                area_type=random.choice(area_type),
                city=random.choice(cities),
            )
        )
    cm.Area.objects.bulk_create(instence_list)
    print("Bulk Insert Done")
