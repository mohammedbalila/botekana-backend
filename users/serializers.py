from rest_framework import serializers

from . import models
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = models.WishlistItem
        fields = '__all__'
        read_only_fields = ['user']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feedback
        exclude = ['date_added']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone']
