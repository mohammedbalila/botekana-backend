from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from . import models
from products.serializers import ProductSerializer


class CartItemCreateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    id = serializers.IntegerField(source='product_id', write_only=True)
    cart = serializers.PrimaryKeyRelatedField(
        queryset=models.Cart.objects.all())

    class Meta:
        model = models.CartItem
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    id = serializers.IntegerField(source='product_id', write_only=True)

    class Meta:
        model = models.CartItem
        fields = '__all__'
        read_only_fields = ['cart']


class CartItemReportSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='cart.id')
    product = serializers.StringRelatedField()
    user = serializers.ReadOnlyField(source='cart.user.id')
    user_name = serializers.StringRelatedField(source='cart.user')
    date_added = serializers.ReadOnlyField(source='cart.date_added')

    class Meta:
        model = models.CartItem
        exclude = ['cart']


class CartReportSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    deliverer = serializers.StringRelatedField()
    date_added = serializers.SerializerMethodField()
    date_finished = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        exclude = ['is_active']
        read_only_fields = ['address', 'zip_code',
                            'payment_method', 'payment_status']

    def get_items(self, obj):
        items = []
        for item in obj.items.all():
            items.append(item.product.name_ar)
        return ','.join(items)

    def get_date_added(self, obj):
        return obj.date_added.strftime("%Y-%m-%d %H:%M")

    def get_date_finished(self, obj):
        if obj.date_finished:
            return obj.date_finished.strftime("%Y-%m-%d %H:%M")
        return None


class CartSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Cart
        fields = '__all__'
        read_only_fields = ['user', 'is_active', 'date_finished']

    def get_user_name(self, obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)


class CartCreateSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = models.Cart
        fields = '__all__'
        read_only_fields = ['user', 'is_active', 'date_finished']

    def create(self, validated_data):
        # Get the request object
        request = self.context.get('request')
        # Cart items
        cart_items = validated_data.pop('items')
        # Create a cart first
        cart = models.Cart.objects.create(**validated_data, user=request.user)

        for cart_item in cart_items:
            try:
                product = models.Product.objects.get(
                    id=cart_item['product_id'])

                # Validate that the color and size of the product are available
                if cart_item['color'] not in product.colors.split(',') or \
                        str(cart_item['size']) not in product.sizes.split(','):
                    raise serializers.ValidationError(
                        {'details': "Color or size not available"})

                # Check if the price is supplied from the client side
                if cart_item.get('price'):
                    price = cart_item.get('price')
                # Else, calculate the price manually.
                else:
                    price = product.price * float(cart_item['quantity'])
                models.CartItem.objects.create(
                    **cart_item, price=price, cart=cart)
            except models.Product.DoesNotExist:
                cart.delete()
                raise serializers.ValidationError(
                    {'details': "Product does not exist"})
        return cart


class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.WishlistItem
        fields = '__all__'
        read_only_fields = ['user']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feedback
        exclude = ['date_added']


class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPermissions
        fields = ['id', 'can_update_products', 'can_update_brands',
                  'can_add_admins', 'can_remove_admins']


class UserSerializer(serializers.ModelSerializer):
    permissions = UserPermissionsSerializer(read_only=False)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone', 'is_staff', 'permissions']

    def update(self, instance, validated_data: dict):
        permissions = validated_data.pop('permissions')
        instance_permissions = instance.permissions
        # 01101352846
        instance_permissions.can_update_products = permissions.get(
            'can_update_products', instance_permissions.can_update_products)
        instance_permissions.can_update_brands = permissions.get(
            'can_update_brands', instance_permissions.can_update_brands)
        instance_permissions.can_add_admins = permissions.get(
            'can_add_admins', instance_permissions.can_add_admins)
        instance_permissions.save()
        instance.save()
        return instance


class UserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    permissions = UserPermissionsSerializer()

    class Meta:
        model = models.User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'phone', 'permissions']

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone': self.validated_data.get('phone', ''),
            'permissions': self.validated_data.get('permissions', {})
        }

    def custom_signup(self, request, user):
        user.phone = self.validated_data.get('phone')
        try:
            models.UserPermissions.objects.create(
                user=user, **self.validated_data.get('permissions'))
        except:
            pass
        user.save()
