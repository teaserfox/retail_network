from rest_framework import serializers

from retail_network.models import Link, Contacts, Product


class LinkSerializer(serializers.ModelSerializer):
    """Сериализатор для модели звена сети"""
    class Meta:
        model = Link  # модель
        fields = '__all__'  # Поля для отображения


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор модели контакты"""

    class Meta:
        model = Contacts # модель
        fields = '__all__'  # Поля для отображения


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели продукты"""

    class Meta:
        model = Product
        fields = '__all__'  # Поля для отображения
