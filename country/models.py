from email.policy import default
from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100)
    land = models.IntegerField(blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    average_age = models.IntegerField(blank=True, null=True)
    economy_type = models.CharField(blank=True, null=True, max_length=50)

    @property
    def city_counts(self):
        return self.cities.count()

    @property
    def area_list(self):
        areas_list = []
        cities = [city.id for city in list(self.cities.all())]
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
    mayor = models.CharField(blank=True, null=True, max_length=100)
    land = models.IntegerField(blank=True, null=True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.city_name

    class Meta:
        db_table = "city"


class Area(models.Model):
    area_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")
    chairman = models.CharField(blank=True, null=True, max_length=100)
    maintain_cost = models.IntegerField(blank=True, null=True)
    area_type = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.area_name

    class Meta:
        db_table = "area"


class Revenue(models.Model):
    date = models.DateField(default=None)
    amount = models.IntegerField()
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name="revenues",
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.area.area_name + " " + str(self.date)

    class Meta:
        db_table = "revenue"
