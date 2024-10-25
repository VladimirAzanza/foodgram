import csv
import io

from rest_framework import renderers

RECIPE_DATA_FILE_HEADERS = ['Ингредиенты', 'Число', 'Измерение']


class PlainTextRenderer(renderers.BaseRenderer):
    media_type = "text/plain"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        text_buffer = io.StringIO()
        text_buffer.write(' '.join(
            header for header in RECIPE_DATA_FILE_HEADERS) + '\n'
        )
        for recipe_data in data:
            text_buffer.write(' '.join(
                str(sd) for sd in list(recipe_data.values())) + '\n'
            )
        return text_buffer.getvalue()


class CSVCartDataRenderer(renderers.BaseRenderer):
    media_type = "text/csv"  # MIME_TYPES
    format = "csv"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        csv_buffer = io.StringIO()
        csv_writer = csv.DictWriter(
            csv_buffer,
            fieldnames=RECIPE_DATA_FILE_HEADERS,
            extrasaction="ignore"
        )
        csv_writer.writeheader()
        for student_data in data:
            csv_writer.writerow(student_data)
        return csv_buffer.getvalue()
