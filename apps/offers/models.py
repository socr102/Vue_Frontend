from django.db import models

from datetime import datetime
import pytz

from apps.receipts.models import Article
from apps.organizations.models import Organization
from apps.user_panel.models import CustomUser


class Offer(models.Model):
    name = models.CharField(max_length=255)
    details = models.CharField(max_length=2000, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    articles = models.ManyToManyField(Article)

    def update_articles(self, with_articles):
        new_articles = set([a.id for a in with_articles])
        prev_articles = set(self.articles.values_list('id', flat=True))

        missing = new_articles.difference(prev_articles)
        if missing:
            self.articles.add(*missing)
        extra = prev_articles.difference(new_articles)
        if extra:
            self.articles.remove(*extra)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.today = datetime.now().replace(tzinfo=pytz.utc)

    @property
    def is_archive(self):
        return self.end_date < self.today

    @property
    def is_active(self):
        return self.end_date > self.today >= self.start_date
