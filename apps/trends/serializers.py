from rest_framework import serializers

from apps.receipts.models import Article, Product

class ArticleTrendSerializer(serializers.ModelSerializer):
    diff = serializers.ReadOnlyField()
    sales_1 = serializers.ReadOnlyField()
    sales_0 = serializers.ReadOnlyField()

    class Meta:
        model = Article
        fields = ("id", "name", "product_id", "sales_1", "sales_0", "diff")
        read_only_fields = ("diff", "id", "name", "sales_1", "sales_0", "product_id")


class ProductTrendSerializer(serializers.ModelSerializer):
    diff = serializers.ReadOnlyField()
    sales_1 = serializers.ReadOnlyField()
    sales_0 = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ("id", "name", "sales_1", "sales_0", "diff", "number")
        read_only_fields = ("diff", "id", "name", "sales_1", "sales_0", "number")
