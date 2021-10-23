from rest_framework import serializers
from django.db import IntegrityError, transaction

import logging

from .models import Audience

logger = logging.getLogger('django')


class TrimAudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ('name', 'id')


class AudienceSerializer(serializers.ModelSerializer):

    UNIQUE_TOGETHER_ERR = ('Audience with a given name'
                           ' already exists in your organization')

    members = serializers.ListSerializer(child=serializers.IntegerField())
    class Meta:
        model = Audience
        fields = ('id', 'name', 'organization', 'members')
        read_only_fields = ('organization',)

    def create(self, validated_data):
        members = validated_data.pop('members')
        audience = Audience(**validated_data)
        audience.organization_id = self.context['request'].user.organization_id
        try:
            with transaction.atomic():
                audience.save()
                audience.members.add(*members)
                audience._members = members
        except IntegrityError:
            raise serializers.ValidationError({'members': "Invalid members"})
        return audience

    def to_representation(self, instance):
        try:
            members = self._members
        except AttributeError:
            members = [i.id for i in instance.members.all()]

        return {
            'id': instance.pk,
            'name': instance.name,
            'organization': instance.organization_id,
            'members': members
        }

    def update(self, audience: Audience, validated_data):
        members = validated_data.pop('members')
        try:
            with transaction.atomic():
                audience = super().update(audience, validated_data)
                if members:
                    audience.update_members(members)
        except IntegrityError:
            raise serializers.ValidationError({'members': "Invalid members"})
        audience._members = members
        return audience

    def validate(self, attrs):
        if self.instance:
            return attrs
        try:
            org_id = self.context['request'].user.organization_id
            Audience.is_unique(org_id, attrs['name'])
        except Audience.DoesNotExist:
            pass
        else:
            logger.error(f'{self.UNIQUE_TOGETHER_ERR}. '
                         f'Audience Name={attrs["name"]} Org={org_id}')
            raise serializers.ValidationError({'name': self.UNIQUE_TOGETHER_ERR})

        return attrs
