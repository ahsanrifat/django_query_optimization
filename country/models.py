from django.db import models

# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=100)

    @property
    def city_counts(self):
        return self.cities.count()

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.country_name


class City(models.Model):
    city_name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities"
    )

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.city_name


class Area(models.Model):
    area_name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.area_name
