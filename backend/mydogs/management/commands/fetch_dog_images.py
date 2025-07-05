from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from mydogs.models import Mydogs
from django.conf import settings
import os
import time
import random
from serpapi import GoogleSearch

SERPAPI_KEY = "1942b91c43c5782960e6c4282110a1ee2ac3a5c3cf71ef0209465466167ea695"


class Command(BaseCommand):
    help = 'Fetches images for dogs from Google Images based on their breed using SerpAPI.'

    def handle(self, *args, **options):
        dogs_images_path = os.path.join(settings.MEDIA_ROOT, 'dogs_images')
        os.makedirs(dogs_images_path, exist_ok=True)

        dogs_to_update = (Mydogs.objects.filter(image__isnull=True) | Mydogs.objects.filter(image='')).exclude(breed__isnull=True).exclude(breed='').exclude(breed__iexact='Unknown')

        if not dogs_to_update.exists():
            self.stdout.write(self.style.SUCCESS('All dogs already have images.'))
            return

        self.stdout.write(f'Found {dogs_to_update.count()} dogs without images. Starting to fetch...')

        for dog in dogs_to_update:
            breed = dog.breed
            if not breed or breed == 'Unknown':
                self.stdout.write(self.style.WARNING(f'Skipping dog with ID {dog.id} due to missing or unknown breed.'))
                continue

            self.stdout.write(f'Searching for an image for breed: {breed}...')
            params = {
                "engine": "google_images",
                "q": f"{breed} dog",
                "api_key": SERPAPI_KEY,
                "ijn": 0,
                "tbm": "isch"
            }
            try:
                search = GoogleSearch(params)
                results = search.get_dict()
                images_results = results.get("images_results", [])
                if not images_results:
                    self.stdout.write(self.style.WARNING(f'No image found for {breed}'))
                    continue
                image_url = images_results[0]["original"]
                self.stdout.write(f'Found image URL: {image_url}')
                # Скачиваем картинку
                import requests
                img_response = requests.get(image_url, timeout=15)
                img_response.raise_for_status()
                file_name = f"{breed.lower().replace(' ', '_')}_{dog.id}.jpg"
                dog.image.save(file_name, ContentFile(img_response.content), save=True)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully downloaded and saved image for {breed} (ID: {dog.id})'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error fetching image for {breed}: {e}'))
            time.sleep(random.uniform(1, 2))
        self.stdout.write(self.style.SUCCESS('Finished fetching images.'))