from django.urls import path

from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserEditView.as_view(), name="user-details"),
    path("carts/", views.CartListView.as_view(), name="cart-list"),
    path("carts/<int:pk>/", views.CartEditView.as_view(),
         name="cart-detail"),
    path("carts/finish/", views.CartFinishView.as_view(), name="cart-finish"),
    path("carts/history/", views.CartHistoryView.as_view(),
         name="cart-history"),
    path("cart_item/", views.CartItemCreateView.as_view(),
         name="cartitem-create"),
    path("cart_item/<int:pk>/", views.CartItemEditView.as_view(),
         name="cartitem-details"),
    path("wishlist/", views.WishlistEditView.as_view(), name="user-wishlist"),
    path("feedback/", views.FeedbackSubmitView.as_view(),
         name="feedback-submit"),
]
