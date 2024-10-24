import csv
import logging

from django.core.management.base import BaseCommand

from ingredients.models import Ingredient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    help = (
        'Import ingredients from a CSV file.'
        'Do not repeat this command more than once.'
        'This command does not check if the ingredient is already created.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', type=str, help='Indicate path to CSV.', required=True
        )

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        ingredients_list = []
        try:
            with open(path, encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    name = row[0]
                    measurement_unit = row[1]
                    ingredient = Ingredient(
                        name=name, measurement_unit=measurement_unit
                    )
                    ingredients_list.append(ingredient)
            Ingredient.objects.bulk_create(ingredients_list)
            logger.info('Импортирование данных прошло успешно!')
        except Exception as e:
            logger.error(f'Ошибка при импорте: {e}')
