from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Spot(models.Model):
    name = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    description = models.TextField(max_length=300)
    latutude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name