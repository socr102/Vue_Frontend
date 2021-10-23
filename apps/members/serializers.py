from rest_framework import serializers

from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member

        fields = ('id',
                  'name',
                  'email',
                  'phone',
                  'sex',
                  'birth_date',
                  'is_active',
                  'external_id',
                  'store'
                  )

        read_only_fields = ('id', 'is_archive', 'store')

    def create(self, validated_data):
        member = Member(**validated_data)
        member.organization_id = self.context['request'].user.organization_id
        member.save()
        return member


class MemberCampaignSerializer(serializers.Serializer):
    order = serializers.ChoiceField(choices=["end_date", "-end_date"],
                                    required=False)
    limit = serializers.IntegerField(min_value=1, required=False)

    def to_representation(self, instance):
        order = instance.get('order')
        return {
            'order': 'DESC' if order and order.startswith('-') else 'ASC',
            'limit': instance.get('limit')
        }
