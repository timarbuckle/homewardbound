from django.db import models


class CatStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    ADOPTED = "adopted", "Adopted"
    PENDING = "pending", "Pending"
    NEW = "new", "New"

# Create your models here.
class Cat(models.Model):
    image_cy = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    adopted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=CatStatus.choices,
        default=CatStatus.AVAILABLE,
    )


class UpdateLog(models.Model):
    last_updated = models.DateTimeField()
    total_cats = models.IntegerField(default=0)
    new_cats = models.IntegerField(default=0)
    adopted_cats = models.IntegerField(default=0)
