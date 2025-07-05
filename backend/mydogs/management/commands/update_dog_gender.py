from django.core.management.base import BaseCommand
from mydogs.models import Mydogs

class Command(BaseCommand):
    help = 'Update gender for dogs by list of ids'

    def add_arguments(self, parser):
        parser.add_argument('--ids', nargs='+', type=int, required=True, help='List of Dog IDs')
        parser.add_argument('--gender', type=str, required=True, help='New gender (male/female)')

    def handle(self, *args, **options):
        ids = options['ids']
        gender = options['gender']

        dogs = Mydogs.objects.filter(id__in=ids)
        count = dogs.update(gender=gender)
        self.stdout.write(self.style.SUCCESS(f'Updated gender to {gender} for {count} dogs with ids: {ids}')) 