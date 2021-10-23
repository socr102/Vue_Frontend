from __future__ import annotations

from django.db import models

from apps.members.models import Member
from apps.organizations.models import Organization

class Audience(models.Model):

    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Member)
    organization = models.ForeignKey(Organization,
                                     on_delete=models.SET_NULL,
                                     null=True)

    class Meta:
        unique_together = ['name', 'organization']

    def update_members(self, with_members: list[int]):
        new_members = set(with_members)
        prev_members = set(self.members.values_list('id', flat=True))

        missing = new_members.difference(prev_members)
        if missing:
            self.members.add(*missing)
        extra = prev_members.difference(new_members)
        if extra:
            self.members.remove(*extra)

    @staticmethod
    def is_unique(organization_id, name):
        return Audience.objects.get(organization_id=organization_id,
                                    name=name)
