import os
from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)
    name_ar = models.CharField(_("name in arabic"), max_length=50)
    class Meta:
        ordering = ['name']
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(_("name"), max_length=50)
    name_ar = models.CharField(_("name in arabic"), max_length=50)
    categories = models.ManyToManyField(Category, related_name="sub_categories")
    class Meta:
        ordering = ['name']
        verbose_name = _("sub category")
        verbose_name_plural = _("sub categories")

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(_("name"), max_length=50)
    name_ar = models.CharField(_("name in arabic"), max_length=50)
    class Meta:
        ordering = ['name']
        verbose_name = _("brand")

    def __str__(self):
        return self.name


def get_upload_path(instance, filename):
    try:
        return os.path.join("product_images/secondary_images/", "%s_%s" % (
            instance.product.name,
            filename))
    except:
        return os.path.join("images/", "%s_%s" % (datetime.now(),filename))


class Product(models.Model):
    name = models.CharField(_("name"), max_length=50)
    name_ar = models.CharField(_("name in arabic"), max_length=50)
    description = models.TextField(_("description"))
    description_ar = models.TextField(_("description in arabic"))
    colors = models.TextField(_("available colors"),
                              help_text="Comma seperated list of available colors",
                              # Validate that they are comma seperated.
                              validators=[RegexValidator(r"^((\w)+,)*\w+$")])
    colors_ar = models.TextField(
        _("available colors in arabic"),
        help_text="Comma seperated list of available colors in arabic",
        validators=[
            # Make sure the colors are comma seperated
            RegexValidator(r"^(([\u0621-\u064a])+,)*[\u0621-\u064a]+$")
        ]
    )
    image = models.ImageField(_("main image"), upload_to=get_upload_path,
                              help_text="Main image for the product")
    price = models.FloatField(_("price"))
    quantity = models.PositiveIntegerField(_("quantity"))
    sku = models.CharField(_("sku"), max_length=40, unique=True)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    sizes = models.TextField(_("size"),
                             help_text="Comma seperated list of available sizes",
                             validators=[RegexValidator(r"^(\d+,)*\d+$")])
    brand = models.ForeignKey(Brand, models.CASCADE, related_name="products",
                              related_query_name="products",
                              verbose_name=_("brand"))
    category = models.ForeignKey(Category, models.CASCADE,
                                 related_name="products",
                                 related_query_name="products",
                                 verbose_name=_("category"))
    sub_category = models.ForeignKey(SubCategory, models.CASCADE,
                                     related_name="products",
                                     related_query_name="products",
                                     verbose_name=_("sub category"))

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(_("image"), upload_to=get_upload_path)
    product = models.ForeignKey("products.Product",  models.CASCADE,
                                related_name='images',
                                related_query_name='images',
                                verbose_name=_("product"),
                                blank=True, null=True)
    category = models.ForeignKey("products.Category",  models.CASCADE,
                                 related_name="image",
                                 related_query_name="image",
                                 verbose_name=_("category"),
                                 blank=True, null=True)
    sub_category = models.ForeignKey("products.SubCategory",  models.CASCADE,
                                     related_name="image",
                                     related_query_name="image",
                                     verbose_name=_("sub category"),
                                     blank=True, null=True)

    def __str__(self):
        return self.id


class Discount(models.Model):
    product = models.ForeignKey(Product, models.CASCADE,
                                related_name="discounts",
                                related_query_name="discounts",
                                verbose_name=_("product"))
    finish_date = models.DateField(_("finish date"))
    percentage = models.PositiveSmallIntegerField(_("percentage"))

    class Meta:
        unique_together = ['product', 'finish_date', 'percentage']
