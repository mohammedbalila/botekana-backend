from django.db import IntegrityError
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response

from . import models, serializers
from .permissions import IsUserOrReadOnly, IsUser


class UserListView(generics.ListAPIView):
    """
    get:
        ### Retrieve list of users.
    """
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_active=True)


class UserEditView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsUserOrReadOnly]
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.is_active = False
            user.save()
            return Response({'success': True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'info': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class WishlistEditView(generics.ListCreateAPIView):
    """
    get:
        ### Retrieve wishlist contents. `Authenticated users only`
    post:
        ### Add new wishlist item.`Authenticated users only`
    delete:
        ### Delete wishlist item. `Authenticated users only`
    """
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WishlistItemSerializer

    def get_queryset(self):
        return models.WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            raise exceptions.ValidationError(
                {'details': "Product is already in wishlist"})

    def delete(self, request, *args, **kwargs):
        try:
            item = models.WishlistItem.objects.get(pk=request.data['pk'])
            item.delete()
            return Response({'success': True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'info': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartListView(generics.ListCreateAPIView):
    """
    get:
        ### List all carts. `Authenticated users only`
    """
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.all()


class FeedbackSubmitView(generics.CreateAPIView):
    """
    post:
        ### Submit feedback.
    """
    serializer_class = serializers.FeedbackSerializer
    queryset = models.Feedback.objects.all()

    def perform_create(self, serializer):
        serializer.save()
