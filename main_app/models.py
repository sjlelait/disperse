from django.db import models

# Create your models here.

class Spot(models.Model):
    name = models.CharField(max_length=100)
    zipcode = models.IntegerField(max_length=5)
    description = models.TextField(max_length=300)
    latutude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name