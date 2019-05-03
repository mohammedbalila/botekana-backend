from django.urls import path

from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/", views.UserEditView.as_view(), name="user-details"),
    path("wishlist/", views.WishlistEditView.as_view(), name="user-wishlist"),
    path("feedback/", views.FeedbackSubmitView.as_view(),
         name="feedback-submit"),
]
