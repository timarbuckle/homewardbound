from datetime import date, timedelta
import httpx
import logging
from typing import cast

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.files.base import ContentFile


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CatStatus(models.TextChoices):
    AVAILABLE = "available", "Available"
    ADOPTED = "adopted", "Adopted"
    PENDING = "pending", "Pending"
    NEW = "new", "New"

class ItemQuerySet(models.QuerySet):
    def recent(self):
        """Returns items updated within the last 24 hours."""
        time_threshold = timezone.now() - timedelta(hours=24)
        return self.filter(last_updated__gte=time_threshold)

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
    image = models.ImageField(upload_to='cats/', null=True, blank=True)
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=CatStatus.choices,
        default=CatStatus.AVAILABLE,
    )

    objects = ItemQuerySet.as_manager()

    @property
    def age(self):
        if not self.birthday:
            return "Unknown"

        today = timezone.now().date()
        diff = today - cast(date, self.birthday)
        years = diff.days // 365
        months = (diff.days % 365) // 30
        if years < 1:
            return f"{months}mo"
        return f"{years}y{months}mo"

    @property
    def clean_breed(self):
        # Remove the word "Domestic" from the breed name
        substring_to_remove = "Domestic "
        if self.breed:
            return self.breed.replace(substring_to_remove, "").strip()
        return self.breed

class UpdateLog(models.Model):
    last_updated = models.DateTimeField()
    total_cats = models.IntegerField(default=0)
    new_cats = models.IntegerField(default=0)
    adopted_cats = models.IntegerField(default=0)


@receiver(post_save, sender=Cat)
def download_image_on_save(sender, instance, created, **kwargs):
    # Only trigger if there's a URL but no local image yet
    if instance.image_url and not instance.image:
        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(instance.image_url, timeout=10.0)
                response.raise_for_status()
                
                # Extract filename
                file_name = instance.image_url.split("/")[-1]
                
                # We use .save(save=False) inside a signal to avoid infinite loops
                instance.image.save(file_name, ContentFile(response.content), save=False)
                
                # Update only the image field to finalize
                instance.save(update_fields=['image'])
                
        except Exception as e:
            # In a production app, you might want to log this to a file
            logger.error(f"Failed to auto-download image for {instance.name}: {e}")