from django.contrib import admin

# Register your models here.
from .models import Spot, Photo

admin.site.register([Spot, Photo])