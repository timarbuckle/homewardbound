import httpx
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from cats.models import Cat

class Command(BaseCommand):
    help = 'Downloads external images and saves them locally'

    def handle(self, *args, **kwargs):
        # Only get cats that don't have a local image yet
        cats = Cat.objects.filter(image=None) #.exclude(image_url='')

        with httpx.Client(follow_redirects=True) as client:
            for cat in cats:
                try:
                    response = client.get(cat.image_url, timeout=10.0)
                    
                    # HTTPX uses raise_for_status() to catch 4xx/5xx errors easily
                    response.raise_for_status()

                    file_name = cat.image_url.split("/")[-1]
                    
                    # Save to the ImageField
                    cat.image.save(file_name, ContentFile(response.content), save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully downloaded {file_name}'))
                
                except httpx.HTTPStatusError as e:
                    self.stdout.write(self.style.ERROR(f'Error response {e.response.status_code} for {cat.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Connection error for {cat.name}: {e}'))