from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# installed Pillow for images
from PIL import Image

# Create your models here.

class Spot(models.Model):
    name = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    description = models.TextField(max_length=300)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='spot_images', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('spot_detail', kwargs={'pk': self.id})

class Photo(models.Model):
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='spot_images', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Photo for spot_id': {self.spot.name} - {self.image.name}"
