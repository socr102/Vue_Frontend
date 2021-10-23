from rest_framework import serializers

from apps.user_panel.serializers import UserListSerializer
from .models import Store, OrderLine, Article, Receipt, Payment, Product

class StoreSerializer(serializers.ModelSerializer):
    """
    C - admin, super_admin
    R - associated_user, admin, super_admin
    U - admin, super_admin
    D - admin, super_admin
    """
    class Meta:
        model = Store
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        store = Store.objects.create(**validated_data)
        user.stores.add(store)
        return store


class ArticleSerializer(serializers.ModelSerializer):
    """
    C - admin, super_admin
    R - user, admin, super_admin
    U - admin, super_admin
    D - admin, super_admin
    """
    class Meta:
        model = Article
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    """
    C - admin, super_admin
    R - associated_user, admin, super_admin
    U - admin, super_admin
    D - admin, super_admin
    """
    class Meta:
        model = Receipt
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    """
    C - admin, super_admin
    R - associated_user, admin, super_admin
    U - admin, super_admin
    D - admin, super_admin
    """
    class Meta:
        model = OrderLine
        fields = '__all__'


class TrimArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'name')


class TrimStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name')


class OrderLineDetailSerializer(OrderLineSerializer):
    article = TrimArticleSerializer(read_only=True)
    store = TrimStoreSerializer(read_only=True)

    class Meta(OrderLineSerializer.Meta):
        pass


class PaymentSerializer(serializers.ModelSerializer):
    """
    C - admin, super_admin
    R - associated_user, admin, super_admin
    U - admin, super_admin
    D - admin, super_admin
    """
    class Meta:
        model = Payment
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    """
    C - admin, super_admin
    R - associated_user, admin, super_admin
    U - admin, super_admin
    D - admin, super_admin
    """
    class Meta:
        model = Product
        fields = '__all__'


class FetchArticleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance['article_id'],
            'name': instance['article__name'],
            'gtin': instance['article__gtin'],
            'product': instance['article__product'],
            'sold_items': instance['sold_items']
        }


class FetchProductSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance['article__product_id'],
            'name': instance['article__product__name'],
            "number": instance['article__product__number'],
            'category': instance['article__product__category'],
            'sold_items': instance['sold_items']
        }


class FetchStoreSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'id': instance['receipt__orderline__store_id'],
            'name': instance['receipt__orderline__store__name'],
            'address': instance['receipt__orderline__store__address'],
            'revenue': instance['revenue']
        }


class ArticlesRecSerializer(serializers.ModelSerializer):
    percent = serializers.ReadOnlyField()
    avg_order_value = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ("id", "name", "product", "percent", "avg_order_value")
        read_only_fields = ("id", "name", "product", "percent", "avg_order_value")


class ProductConnectionSerializer(serializers.Serializer):
    product_ids = serializers.ListField(child=serializers.IntegerField(),
                                        read_only=True)
    correlation = serializers.FloatField(read_only=True)

    def to_representation(self, instance):
        return {
            'product_ids': instance[0],
            'correlation': instance[1]
        }


class ArticleRecInputSerializer(serializers.Serializer):
    article = serializers.ListField(child=serializers.IntegerField(),
                                    required=True)

    class Meta:
        read_only_fields = ('article',)


class ProdRecInputSerializer(serializers.Serializer):
    product = serializers.ListField(child=serializers.IntegerField(),
                                    required=True)

    class Meta:
        read_only_fields = ('product',)


class ProductRecSerializer(serializers.ModelSerializer):
    percent = serializers.ReadOnlyField()
    avg_order_value = serializers.ReadOnlyField()
    recs = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ("id", "name", "number",
                  "percent", "avg_order_value", "recs")
        read_only_fields = ("id", "name", "number",
                            "percent", "avg_order_value", "recs")


class TrimArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('name', 'id')


class ArticleConnectionSerializer(serializers.Serializer):
    articles = serializers.ListField(child=TrimArticleSerializer(),
                                        read_only=True)
    correlation = serializers.FloatField(read_only=True)

    def to_representation(self, instance):
        return {
            'articles': instance[0],
            'correlation': instance[1]
        }

class ArticleBoughtTogetherSerializer(serializers.Serializer):

    article_id = serializers.ReadOnlyField()
    article_name = serializers.ReadOnlyField()
    category = serializers.ReadOnlyField()
    total_bt = serializers.ReadOnlyField()

    def to_representation(self, instance):
        return { 
            'article_id': instance[0],
            'article_name': instance[1],
            'category': instance[2],
            'total_bt': instance[3]
        }
