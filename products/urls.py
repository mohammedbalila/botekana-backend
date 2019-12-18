from django.urls import path

from . import views


urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
    path("<int:pk>/", views.ProductEditView.as_view(), name="product-detail"),
    path("<int:product_id>/images/", views.ImageCreateView.as_view(),
         name="product-image-create"),
    path("has_discount/", views.DiscountedProductListView.as_view(),
         name="discountedproducts-list"),
    path("categories/", views.CategoryListView.as_view(),
         name="category-list"),
    path("categories/<int:pk>/", views.CategoryEditView.as_view(),
         name="category-detail"),
    path("categories/<int:category_id>/image/",
         views.ImageCreateView.as_view(),
         name="category-image-create"),
     path("categories/<int:category_id>/image/", views.ImageEditView.as_view(),
         name="category-image-detail"),
    path("sub-categories/", views.SubCategoryListView.as_view(),
         name="subcategory-list"),
    path("sub-categories/<int:pk>/",
         views.SubCategoryEditView.as_view(), name="subcategory-detail"),
     path("sub-categories/<int:sub_category_id>/image/",
         views.ImageCreateView.as_view(), name="subcategory-image-detail"),
             path("sub-categories/<int:sub_category_id>/image/",
         views.ImageEditView.as_view(), name="subcategory-image-detail"),
    path("brands/", views.BrandListView.as_view(), name="brand-list"),
    path("brands/<int:pk>/", views.BrandEditView.as_view(),
         name="brand-detail"),
    path("discounts/", views.DiscountListView.as_view(), name="discount-list"),
    path("discounts/<int:pk>/", views.DiscountEditView.as_view(),
         name="discount-detail"),
         path("images/<int:pk>/", views.ImageEditView.as_view(),
         name="image-delete")
]
