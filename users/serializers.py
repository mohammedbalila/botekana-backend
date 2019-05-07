from rest_framework import serializers

from . import models
from products.serializers import ProductSerializer


class CartItemCreateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    cart = serializers.PrimaryKeyRelatedField(
        queryset=models.Cart.objects.all())

    class Meta:
        model = models.CartItem
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.CartItem
        fields = '__all__'
        read_only_fields = ['cart']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Cart
        fields = '__all__'
        read_only_fields = ['user', 'is_active', 'date_finished']


class CartCreateSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = '__all__'
        read_only_fields = ['user', 'is_active', 'date_finished']

    def create(self, validated_data):
        # Get the request object
        request = self.context.get('view').request
        # Cart items
        cart_items = validated_data.pop('items')
        # Create a cart first
        cart = models.Cart.objects.create(**validated_data, user=request.user)

        for cart_item in cart_items:
            try:
                product = models.Product.objects.get(
                    id=cart_item['product_id'])
                if cart_item['color'] not in product.colors.split(',') or \
                        str(cart_item['size']) not in product.sizes.split(','):
                    raise serializers.ValidationError(
                        {'details': "Color or size not available"})
                price = product.price * float(cart_item['quantity'])
                models.CartItem.objects.create(
                    **cart_item, price=price, cart=cart)
            except models.Product.DoesNotExist:
                cart.delete()
                raise serializers.ValidationError(
                    {'details': "Product does not exist"})
        return cart

    # def update(self, instance, validated_data):
    #     # Get the request object
    #     request = self.context.get('view').request
    #     # Cart items
    #     cart_items = validated_data.pop('items')
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)

    #     for cart_item in cart_items:
    #         try:
    #             product = cart_item['product']
    #             if cart_item['color'] not in product.colors.split(',') or \
    #                     str(cart_item['size']) not in product.sizes.split(','):
    #                 raise serializers.ValidationError(
    #                     {'details': "Colors or size not available"})
    #             price = product.price * float(cart_item['quantity'])
    #             models.CartItem.objects.filter(
    #                 id=cart_item.pop('id')).update(**cart_item)
    #         except models.Product.DoesNotExist:
    #             raise serializers.ValidationError(
    #                 {'details': "Product does not exist"})
    #     instance.save()
    #     return instance


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
