from django.core.management.base import BaseCommand
from mydogs.models import Mydogs
import random

class Command(BaseCommand):
    help = 'Randomly assign gender=female to a portion of dogs'

    def add_arguments(self, parser):
        parser.add_argument('--percent', type=float, default=50, help='Percent of dogs to set as female (default 50)')

    def handle(self, *args, **options):
        percent = options['percent']
        all_ids = list(Mydogs.objects.values_list('id', flat=True))
        n = int(len(all_ids) * percent / 100)
        if n == 0:
            self.stdout.write(self.style.WARNING('No dogs selected for update.'))
            return
        female_ids = random.sample(all_ids, n)
        updated = Mydogs.objects.filter(id__in=female_ids).update(gender='female')
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} dogs to gender=female (percent={percent}%)')) 