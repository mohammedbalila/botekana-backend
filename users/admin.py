from django.contrib import admin

from . import models


admin.site.register([models.User, models.Feedback,
                     models.Cart, models.CartItem,
                     models.WishlistItem])
