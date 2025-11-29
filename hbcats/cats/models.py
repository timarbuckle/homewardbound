from django.db import models


# Create your models here.
class Cat(models.Model):
    image_cy = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
