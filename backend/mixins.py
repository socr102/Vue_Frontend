from django.http import Http404

from apps.campaigns.permissions import CampaignPermission
from apps.campaigns.models import Campaign
from apps.members.permissions import MemberPermission
from apps.members.models import Member

class LookupMixin:
    def get_object(self):
        try:
            obj = self._model.objects.get(pk=self.kwargs.get(self.lookup_field))
        except self._model.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

    def get_objects(self):
        try:
            campaign = Campaign.objects.get(pk=self.kwargs.get('campaign_id'))
            member = Member.objects.get(pk=self.kwargs.get('pk'))
        except (Campaign.DoesNotExist, Member.DoesNotExist) as e:
            raise Http404
        CampaignPermission().has_object_permission(self.request, self, campaign)
        MemberPermission().has_object_permission(self.request, self, member)
        return campaign, member
