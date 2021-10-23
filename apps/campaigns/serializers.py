import logging

from rest_framework import serializers

from .models import Campaign
from apps.offers.serializers import TrimOfferSerializer
from apps.audience.serializers import TrimAudienceSerializer

logger = logging.getLogger('django')
RESOURCE_NOT_ALLOWED_ERR = 'Invalid pk \"{pk}\" - object does not exist'


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'name', 'offer', 'organization',
                  'audience', 'metadata', 'is_archive', 'is_active')
        read_only_fields = ('organization', 'id', 'metadata',
                            'is_archive', 'is_active')
        extra_kwargs = {'offer': {'required': True},
                        'audience': {'required': True}
                       }

    def create(self, validated_data):
        campaign = Campaign(**validated_data)
        campaign.organization_id = self.context['request'].user.organization_id
        campaign.save()
        return campaign

    def to_representation(self, campaign):
        _repr = super().to_representation(campaign)
        _repr['offer'] = TrimOfferSerializer(campaign.offer).data
        _repr['audience'] = TrimAudienceSerializer(campaign.audience).data
        return _repr

    def validate_offer(self, offer):
        user = self.context['request'].user
        if offer.organization_id != user.organization_id:
            error = RESOURCE_NOT_ALLOWED_ERR.format(pk=offer.id)
            logger.error(f'Offer resource permission rejected: {error}')
            raise serializers.ValidationError(error)
        return offer

    def validate_audience(self, audience):
        user = self.context['request'].user
        if audience.organization_id != user.organization_id:
            error = RESOURCE_NOT_ALLOWED_ERR.format(pk=audience.id)
            logger.error(f'Audience resource permission rejected: {error}')
            raise serializers.ValidationError(error)
        return audience


class CampaignDuplicateSerializer(CampaignSerializer):
    def create(self, campaign):
        campaign.pk = None
        campaign.metadata = {}
        campaign.save()
        return campaign
