from datetime import datetime
# import simplify

from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, Http404
from django.contrib.auth.models import AnonymousUser
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, exceptions, filters
from rest_framework.response import Response

from . import models, serializers
from .permissions import (IsUserOrReadOnly, IsUser,
                          IsOwner, IsOwnerOrAdminReadOnly,
                          IsUserOrAdminReadOnly)


# # QNB Simplify API keys.
# simplify.public_key = 'sbpb_NTUxYTAwNjctZjM4MS00YjQ1LWE1NjEtMWJhMjQ1ZjZiMDZh'
# simplify.private_key = (
#     'b/cr9oFaWMz1dnqqS6F107lOjiEuPxMxIdYrPRU9g2B5YFFQL0ODSXAOkNtXTToq'
# )


class UserListView(generics.ListAPIView):
    """
    get:
        ### Retrieve list of users.
    """
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
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
            if kwargs.get("id"):
                get_object_or_404(models.Product.objects.all(),
                                  pk=request.data['pk']).wishlist_items\
                    .get(user=kwargs.get("id"))\
                    .delete()
            else:
                get_object_or_404(models.Product.objects.all(),
                                  pk=request.data['pk']).wishlist_items\
                    .get(user=request.user)\
                    .delete()
            return Response({'success': True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'info': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartFilter(rest_framework.FilterSet):
    added_before = rest_framework.DateFilter(field_name='date_added',
                                             lookup_expr='lte')
    added_after = rest_framework.DateFilter(field_name='date_added',
                                            lookup_expr='gte')
    finished_before = rest_framework.DateFilter(field_name='date_finished',
                                                lookup_expr='lte')
    finished_after = rest_framework.DateFilter(field_name='date_finished',
                                               lookup_expr='gte')
    is_not_submitted = rest_framework.BooleanFilter(field_name='date_added',
                                                    lookup_expr='isnull')
    is_not_finished = rest_framework.BooleanFilter(field_name='date_finished',
                                                   lookup_expr='isnull')

    class Meta:
        model = models.Cart
        fields = ['is_active', 'payment_method', 'country',
                  'zip_code', 'is_not_submitted', 'is_not_finished',
                  'added_before', 'added_after',
                  'finished_before', 'finished_after']


class CartListView(generics.ListAPIView):
    """
    get:
        ### List all carts. `Admin users only`
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['address', 'country']
    filterset_class = CartFilter


class UserCartListView(generics.ListCreateAPIView):
    """
    get:
        ### List all carts. `Authenticated users only`
    post:
        ### Create new cart. `Authenticated users only`
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartFilter

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.kwargs['pk'])

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


class CartFinishView(generics.views.APIView):
    """
    get:
        ### Submit Cart.
    post:
        ### Finish Cart.
    """
    permission_classes = [IsOwner]
    queryset = models.Cart.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cart = get_object_or_404(self.queryset, pk=kwargs['pk'])
            # Make sure the cart is not submitted already.
            if cart.date_added:
                raise Exception("Cart already submitted")

            # Get the products in the cart
            products = models.Product.objects.select_for_update().filter(
                cartitem__cart=cart)

            with transaction.atomic():
                # Validate order.
                for product in products:
                    # Calculate the new quantity
                    product.quantity -= cart.items.get(product=product)\
                        .quantity
                    # Check if there's enough quantity for the order
                    if product.quantity < 0:
                        raise Exception(
                            "Not enough quantity for {0};"
                            "كمية غير كافية للمنتج {0}".format(product))
                # Save the new quantities.
                for product in products:
                    product.save()
                # Update cart.
                cart.date_added = datetime.now()
                cart.save()

            return Response({'success': True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'details': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            cart = get_object_or_404(self.queryset, pk=kwargs['pk'])
            if not cart.is_active:
                raise Exception("Cart already finished")

            # Get the total price of the cart.
            price = cart.items.aggregate(Sum('price'))['price__sum']
            # payment = simplify.Payment.create({
            #     "token": request.data['token'],
            #     "amount": price,
            #     "currency": "QAR"
            # })
            # # Verify that the payment is done.
            # if payment.paymentStatus != 'APPROVED':
            #     raise Exception('Payment not approved')

            # Update cart.
            cart.date_finished = datetime.now()
            cart.is_active = False
            cart.save()
            return Response({'success': True}, status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False,
                             'details': e.__str__()},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class FeedbackListView(generics.ListCreateAPIView):
    """
    get:
        ### List feedbacks.
    post:
        ### Submit feedback.
    """
    serializer_class = serializers.FeedbackSerializer
    queryset = models.Feedback.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['message']
    filterset_fields = ['email', 'date_added']
