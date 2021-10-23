from django.db.models import Q

from datetime import datetime
import pytz

def Q_is_active_offer(value,
                      start_date="start_date",
                      end_date="end_date"):
    now = datetime.now().replace(tzinfo=pytz.utc)
    if value:
        return Q(**{f'{end_date}__gte': now}) &\
               Q(**{f'{start_date}__lte': now})
    else:
        return Q(**{f'{start_date}__gt': now}) |\
               Q(**{f'{end_date}__lt': now})

def Q_is_archive_offer(value, end_date="end_date"):
    q = f'{end_date}__lt' if value else f'{end_date}__gte'
    now = datetime.now().replace(tzinfo=pytz.utc)
    return {q: now}
