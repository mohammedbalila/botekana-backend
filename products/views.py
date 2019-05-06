from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import serializers, models


class ProductListView(generics.ListCreateAPIView):
    """
    get:
        ### List all products.
    post:
        ### Create new product.
    """
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
    serializer_class = serializers.BrandSerializer
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
    serializer_class = serializers.CategorySerializer
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
    serializer_class = serializers.SubCategorySerializer
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
