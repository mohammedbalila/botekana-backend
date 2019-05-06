from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from products.models import Product


class User(AbstractUser):
    phone = models.CharField(_("Phone Number"), max_length=20, unique=True,
                             validators=[RegexValidator(r"^[+]*[(]{0,1}[0-9]"
                                                        "{1,4}[)]{0,1}"
                                                        "[-\s\./0-9]*$")],
                             blank=True, null=True)


class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="carts",
                             related_query_name="carts",
                             verbose_name=_("user"))
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    is_active = models.BooleanField(_("is active"), default=True)
    date_finished = models.DateTimeField(
        _("date finished"), blank=True, null=True)
    country = models.CharField(
        _("country"), max_length=50, blank=True, null=True)
    address = models.TextField(_("address"), blank=True, null=True)
    zip_code = models.PositiveIntegerField(
        _("zip code"), blank=True, null=True)
    payment_method = models.CharField(_("payment method"), max_length=2,
                                      choices=[('c', 'Cash'), ('v', 'Visa')],
                                      blank=True, null=True)

    class Meta:
        ordering = ['date_added']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, models.CASCADE, related_name="items",
                             related_query_name="items",
                             verbose_name=_("cart"))
    product = models.ForeignKey(
        Product, models.CASCADE, verbose_name=_("product"))
    quantity = models.PositiveSmallIntegerField(_("quantity"))
    color = models.CharField(_("color"), max_length=50)
    size = models.PositiveSmallIntegerField(_("Size"), blank=True, null=True)
    price = models.FloatField(_("price"))

    def __str__(self):
        return self.product.name


class WishlistItem(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="wishlist_items",
                             related_query_name="wishlist_items",
                             verbose_name=_("user"))
    product = models.ForeignKey(
        Product, models.CASCADE, verbose_name=_("product"))
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)

    class Meta:
        ordering = ['date_added']
        unique_together = ['user', 'product']

    def __str__(self):
        return self.product.name


class Feedback(models.Model):
    email = models.EmailField(_("email"))
    message = models.TextField(_("feedback message"))
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.content[:50]
