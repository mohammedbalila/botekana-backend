from rest_framework import serializers

from . import models


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['image']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    brand = serializers.StringRelatedField()
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    sub_category = serializers.PrimaryKeyRelatedField(read_only=True)
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    colors_ar = serializers.SerializerMethodField()
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def get_sizes(self, obj):
        return map(int, obj.sizes.split(','))

    def get_colors(self, obj):
        return obj.colors.split(',')

    def get_colors_ar(self, obj):
        return obj.colors_ar.split(',')


class ProductCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        files = self.context.get('view').request.FILES
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


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SubCategory
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Category
        fields = '__all__'
