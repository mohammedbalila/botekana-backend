from datetime import datetime

from django.db import IntegrityError
from rest_framework import generics, permissions, status, exceptions
from rest_framework.response import Response

from . import models, serializers
from .permissions import (IsUserOrReadOnly, IsUser,
                          IsOwner, IsOwnerOrAdminReadOnly,
                          IsUserOrAdminReadOnly)


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
        if self.kwargs.get('pk'):
            return models.WishlistItem.objects.filter(user=self.kwargs['pk'])
        return models.WishlistItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            raise exceptions.ValidationError(
                {'details':
                 "Product does not exist or is already in wishlist"})

    def delete(self, request, *args, **kwargs):
        try:
            models.WishlistItem.objects.get(pk=request.data['pk']).delete()
            return Response({'success': True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'info': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartListView(generics.ListCreateAPIView):
    """
    get:
        ### List all carts. `Authenticated users only`
    post:
        ### Create new cart. `Authenticated users only`
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return models.Cart.objects.filter(user=self.kwargs['pk'],
                                              is_active=True)
        return models.Cart.objects.filter(user=self.request.user,
                                          is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CartCreateSerializer
        return serializers.CartSerializer


class CartEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve cart content.
    put:
        ### Edit cart content.
    patch:
        ### Edit cart content.
    delete:
        ### Cancel cart.
    """
    permission_classes = [IsOwnerOrAdminReadOnly]
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.all()


class CartFinishView(generics.DestroyAPIView):
    """
    delete:
        ### Finish cart.
    """
    permission_classes = [IsOwner]
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.all()

    def perform_destroy(self, instance):
        instance.date_finished = datetime.now()
        instance.is_active = False
        instance.save()


class CartHistoryView(generics.ListAPIView):
    """
    get:
        ### View finished and cancelled carts.
    """
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return models.Cart.objects.filter(user=self.kwargs['pk'],
                                              date_finished__isnull=True)
        return models.Cart.objects.filter(user=self.request.user)\
            .exclude(date_finished__isnull=True)


class CartItemCreateView(generics.CreateAPIView):
    """
    post:
        ### Create new cart item.
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.CartItemCreateSerializer
    queryset = models.CartItem.objects.all()


class CartItemEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        ### Retrieve cart item content.
    put:
        ### Edit cart item content.
    patch:
        ### Edit cart item content.
    delete:
        ### Delete cart item.
    """
    permission_classes = [IsOwner]
    serializer_class = serializers.CartItemSerializer
    queryset = models.CartItem.objects.all()

    def perform_update(self, serializer):
        product = models.Product.objects.get(
            id=serializer.validated_data['product_id'])
        price = product.price * \
            float(serializer.validated_data['quantity'])
        serializer.save(price=price)


class FeedbackSubmitView(generics.CreateAPIView):
    """
    post:
        ### Submit feedback.
    """
    serializer_class = serializers.FeedbackSerializer
    queryset = models.Feedback.objects.all()

    def perform_create(self, serializer):
        serializer.save()
