from django.contrib import admin
from .models import Country, City, Area, Revenue


# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Revenue)
