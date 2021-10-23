from django.conf import settings

from backend import utils

DATE_FORMATS = settings.REST_FRAMEWORK['DATETIME_INPUT_FORMATS']

class DateRangeMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields['date'].fields[0].input_formats = DATE_FORMATS
        self.form.fields['date'].fields[-1].input_formats = DATE_FORMATS
