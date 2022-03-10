from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100)

    @property
    def city_counts(self):
        return self.cities.count()

    @property
    def area_list(self):
        areas_list = []
        cities = [city.id for city in list(self.cities.all())]
        # for city in cities:
        #     [
        #         areas_list.append(area.area_name + " (" + city.city_name + ")")
        #         for area in city.areas.all()
        #     ]
        # return areas_list
        areas = Area.objects.filter(city__in=cities)
        return areas

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.country_name

    class Meta:
        db_table = "country"


class City(models.Model):
    city_name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.city_name

    class Meta:
        db_table = "city"


class Area(models.Model):
    area_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.area_name

    class Meta:
        db_table = "area"


class Revenue(models.Model):
    date = models.DateField(default=None)
    amount = models.IntegerField()
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="revenues"
    )

    def __str__(self):
        return self.country.country_name + " " + str(self.date)

    class Meta:
        db_table = "revenue"
