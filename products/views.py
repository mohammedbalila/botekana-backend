from datetime import datetime

from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from . import serializers, models, filters as custom_filters


class ProductListView(generics.ListCreateAPIView):
    """
    get:
        ### List all products.
    post:
        ### Create new product.
    """
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'name_ar', 'description', 'description_ar',
                     'brand__name', 'sku']
    filter_class = custom_filters.ProductFilter
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProductSerializer
        return serializers.ProductCreateSerializer


class ProductEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve product info.
    put:
        ### Update product info.
    patch:
        ### Update product info.
    delete:
        ### Delete product.
    """
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProductSerializer
        return serializers.ProductCreateSerializer


class DiscountedProductListView(generics.ListAPIView):
    """
    get:
        ### List discounted products.
    """
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(
            discounts__finish_date__gt=datetime.now()
        )


class BrandListView(generics.ListCreateAPIView):
    """
    get:
        ### List all brands.
    post:
        ### Create new brand.
    """
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()


class BrandEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve brand info.
    put:
        ### Update brand info.
    patch:
        ### Update brand info.
    delete:
        ### Delete brand.
    """
    serializer_class = serializers.BrandEditSerializer
    queryset = models.Brand.objects.all()


class CategoryListView(generics.ListCreateAPIView):
    """
    get:
        ### List all categories.
    post:
        ### Create new category.
    """
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class CategoryEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve category info.
    put:
        ### Update category info.
    patch:
        ### Update category info.
    delete:
        ### Delete category.
    """
    serializer_class = serializers.CategoryEditSerializer
    queryset = models.Category.objects.all()


class SubCategoryListView(generics.ListCreateAPIView):
    """
    get:
        ### List all sub categories.
    post:
        ### Create new sub category.
    """
    serializer_class = serializers.SubCategorySerializer
    queryset = models.SubCategory.objects.all()


class SubCategoryEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve sub category info.
    put:
        ### Update sub category info.
    patch:
        ### Update sub category info.
    delete:
        ### Delete sub category.
    """
    serializer_class = serializers.SubCategoryEditSerializer
    queryset = models.SubCategory.objects.all()


class DiscountListView(generics.ListCreateAPIView):
    """
    get:
        ### List dicounts.
    post:
        ### Create new discount.
    """
    serializer_class = serializers.DiscountSerializer
    queryset = models.Discount.objects.all()


class DiscountEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve discount info.
    put:
        ### Edit discount info.
    patch:
        ### Edit discount info.
    delete:
        ### Delete discount.
    """
    serializer_class = serializers.DiscountSerializer
    queryset = models.Discount.objects.all()

class ImageCreateView(generics.views.APIView):
    """
    post:
        ### Create image and associate with product.
    """
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            for image in request.FILES.values():
                models.Image.objects.create(
                    image=image, **kwargs)
            return Response({'success': True}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'details': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class ImageEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
        ### Delete image.
    """
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()

    def get_object(self):
        return models.Image.objects.get(**self.kwargs)