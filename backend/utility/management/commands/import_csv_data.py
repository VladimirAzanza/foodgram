import csv
import itertools
import logging

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = (
        'Import ingredients from a CSV file.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', type=str, help='Indicate path to CSV.', required=True
        )

    def ingredient_generator(self, reader):
        for row in reader:
            name, measurement_unit = row
            yield Ingredient(
                name=name, measurement_unit=measurement_unit
            )

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        try:
            with open(path, encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                while True:
                    batch = list(
                        itertools.islice(
                            self.ingredient_generator(reader), 200
                        )
                    )
                    if not batch:
                        break
                    Ingredient.objects.bulk_create(batch)
            logger.info('Импортирование данных прошло успешно!')
        except Exception as e:
            logger.error(f'Ошибка при импорте: {e}')
