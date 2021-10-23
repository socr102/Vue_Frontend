from rest_framework import serializers

from apps.receipts.serializers import TrimArticleSerializer
from .models import Offer


class TrimOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('name', 'id')


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        read_only_fields = ('organization',
                            'created_by',
                            'is_archive',
                            'is_active')
        fields = ('id',
                  'name',
                  'details',
                  'start_date',
                  'end_date',
                  'is_active',
                  'is_archive',
                  'created_by',
                  'articles',
                  'organization',
                  )

    def to_representation(self, offer):
        _repr = super().to_representation(offer)
        _repr['articles'] = TrimOfferSerializer(offer.articles, many=True).data
        return _repr

    def create(self, validated_data):
        articles = validated_data.pop('articles')
        offer = Offer(**validated_data)
        offer.created_by = self.context['request'].user
        offer.organization_id = self.context['request'].user.organization_id
        offer.save()
        offer.articles.add(*articles)
        return offer

    def update(self, offer, validated_data):
        articles = validated_data.get('articles')
        offer = super().update(offer, validated_data)

        if articles:
            offer.update_articles(articles)

        return offer
