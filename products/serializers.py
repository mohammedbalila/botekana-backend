from datetime import datetime
from rest_framework import serializers

from . import models


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image', 'product', 'category', 'sub_category']
        extra_kwargs = { 
            'product': { 'write_only': True },
            'category': { 'write_only': True },
            'sub_category': { 'write_only': True }
            }


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    brand = serializers.PrimaryKeyRelatedField(read_only=True)
    brand_name = serializers.StringRelatedField(
        read_only=True, source='brand')
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True)
    sub_category = serializers.PrimaryKeyRelatedField(read_only=True)
    sub_category_name = serializers.CharField(
        source='sub_category.name', read_only=True)
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    colors_ar = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)
    discounts = serializers.SerializerMethodField()
    # wishlist_id = serializers.SerializerMethodField()
    in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_sizes(self, obj):
        return map(int, obj.sizes.split(','))

    def get_colors(self, obj):
        return obj.colors.split(',')

    def get_colors_ar(self, obj):
        return obj.colors_ar.split(',')

    def get_discounts(self, obj):
        objs = obj.discounts.filter(finish_date__gt=datetime.now())
        return DiscountSerializer(objs, many=True).data

    def get_in_wishlist(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return bool(obj.wishlist_items.filter(user=user))

    # def get_wishlist_id(self, obj):
    #     user = self.context.get('request').user
    #     if not user.is_authenticated:
    #         return None
    #     return obj.wishlist_items.


class ProductCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        files = self.context.get('request').FILES
        files.pop('image')
        product = models.Product.objects.create(**validated_data)

        for image in files.values():
            models.Image.objects.create(product=product, image=image)
        return product


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Brand
        fields = '__all__'


class BrandEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Brand
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = '__all__'

class SubCategoryEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = models.SubCategory
        fields = '__all__'
    def get_image(self, obj: models.Category):
        return ImageSerializer(obj.image.last(),
                               context={
                                   'request': self.context.get('request')
        }).data['image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class CategoryEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = models.Category
        fields = '__all__'
    def get_image(self, obj: models.Category):
        return ImageSerializer(obj.image.last(),
                               context={
                                   'request': self.context.get('request')
        }).data['image']