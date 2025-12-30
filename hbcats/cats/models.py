from django.db import models
from django.utils import timezone


class CatStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    ADOPTED = "adopted", "Adopted"
    PENDING = "pending", "Pending"
    NEW = "new", "New"


# Create your models here.
class Cat(models.Model):
    image_cy = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, default="Unknown")
    birthday = models.DateField(null=True, blank=True, default=timezone.now)
    breed = models.CharField(max_length=25, default="Unknown")
    primary_color = models.CharField(max_length=25, default="Unknown")
    intake_date = models.DateField(null=True, blank=True, default=timezone.now)
    location = models.CharField(max_length=25, default="Unknown")
    image_url = models.URLField()
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=CatStatus.choices,
        default=CatStatus.AVAILABLE,
    )

    @property
    def age(self):
        if not self.birthday:
            return "Unknown"
        
        today = timezone.now().date()
        diff = today - self.birthday
        years = diff.days // 365
        months = (diff.days % 365) // 30
        if years < 1:
            return f"{months}mo"
        return f"{years}y{months}mo"


class UpdateLog(models.Model):
    last_updated = models.DateTimeField()
    total_cats = models.IntegerField(default=0)
    new_cats = models.IntegerField(default=0)
    adopted_cats = models.IntegerField(default=0)
