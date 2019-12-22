from django.urls import path

from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserEditView.as_view(), name="user-details"),
    path("<int:pk>/carts/", views.UserCartListView.as_view(), name="user-carts"),
    path("<int:id>/wishlist/", views.WishlistEditView.as_view(),
         name="user-wishlist"),
    path("carts/", views.CartListView.as_view(), name="cart-list"),
    path("carts/<int:pk>/", views.CartEditView.as_view(),
         name="cart-detail"),
    path("carts/finish/", views.CartFinishView.as_view(), name="cart-finish"),
    path("cart_item/", views.CartItemCreateView.as_view(),
         name="cartitem-create"),
    path("cart_item/<int:pk>/", views.CartItemEditView.as_view(),
         name="cartitem-details"),
    path("wishlist/", views.WishlistEditView.as_view(), name="user-wishlist"),
    path("feedback/", views.FeedbackListView.as_view(),
         name="feedback-submit"),
     path("misc/", views.MiscView.as_view())
]
